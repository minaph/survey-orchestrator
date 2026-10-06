#!/usr/bin/env python3
"""Preserve independent Codex sessions and immutable records for each round."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


EVALUATION_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = EVALUATION_ROOT.parents[1]
SKILL_ROOTS = ("SKILL.md", "references", "scripts", "assets", "agents")
SETTINGS = {
    "model": "gpt-6-luna",
    "reasoning_effort": "high",
    "profile": None,
    "sandbox_mode": "workspace-write",
    "network_access": True,
    "approval": "approve-for-me",
}
WORKSPACE_INSTRUCTIONS = """# Evaluation Workspace

Use the supplied task materials within this workspace. Do not explore other
runs or supervisor records. Standard system tools and necessary installed
skills may be used. Treat SKILL.md, references/, scripts/, assets/, agents/,
and corpus/ as read-only inputs.
Write your own artifacts under outputs/. Select the artifact format yourself.
Keep the task's substantive decisions in your own judgment and report the
artifact paths and the verification you performed in your final response.
"""


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def files_under(root):
    return sorted(path for path in root.rglob("*") if path.is_file()
                  and "__pycache__" not in path.parts and path.suffix != ".pyc")


def copy_verified(source, target, relative, category):
    if source.is_symlink():
        raise ValueError(f"Input symlinks require explicit handling: {source}")
    before = digest(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if digest(source) != before or digest(target) != before:
        raise ValueError(f"Input changed during copy: {source}")
    return {"path": str(relative), "sha256": before,
            "size_bytes": target.stat().st_size, "category": category}


def freeze():
    destination = EVALUATION_ROOT / "snapshot"
    manifest_path = EVALUATION_ROOT / "runtime/snapshot-manifest.json"
    if destination.exists() or manifest_path.exists():
        raise ValueError("Snapshot already exists; do not overwrite the frozen skill")
    destination.mkdir()
    records = []
    for name in SKILL_ROOTS:
        source = REPOSITORY_ROOT / name
        if not source.exists():
            raise ValueError(f"Missing skill input: {source}")
        paths = [source] if source.is_file() else files_under(source)
        for path in paths:
            relative = path.relative_to(REPOSITORY_ROOT)
            records.append(copy_verified(path, destination / relative, relative, "skill"))
    manifest = {"created_at": now(), "copied_roots": list(SKILL_ROOTS),
                "excluded_roots": ["tmp", "audit", "evaluations", "__pycache__"],
                "files": records, "file_count": len(records)}
    write_json(manifest_path, manifest)
    print(json.dumps({"snapshot": str(destination), "files": len(records),
                      "manifest_sha256": digest(manifest_path)}))


def validate_inputs(workspace, records):
    for record in records:
        path = workspace / record["path"]
        if not path.is_file() or digest(path) != record["sha256"]:
            raise ValueError(f"Frozen input changed or disappeared: {path}")


def run_path(run):
    return EVALUATION_ROOT / f"run-{run}"


def prepare(run, corpus):
    directory = run_path(run)
    snapshot = EVALUATION_ROOT / "snapshot"
    manifest_path = EVALUATION_ROOT / "runtime/snapshot-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    corpus = corpus.resolve()
    if not corpus.is_dir() or not files_under(corpus):
        raise ValueError("The final corpus must be a nonempty directory")
    if directory.exists():
        raise ValueError("Run already exists; do not replace its workspace or records")
    workspace = directory / "workspace"
    workspace.mkdir(parents=True)
    records = []
    for record in manifest["files"]:
        relative = Path(record["path"])
        source = snapshot / relative
        if digest(source) != record["sha256"]:
            raise ValueError(f"Snapshot hash mismatch: {source}")
        records.append(copy_verified(source, workspace / relative, relative, "skill"))
    for source in files_under(corpus):
        relative = Path("corpus") / source.relative_to(corpus)
        records.append(copy_verified(source, workspace / relative, relative, "paper"))
    (workspace / "AGENTS.md").write_text(WORKSPACE_INSTRUCTIONS)
    (workspace / "outputs").mkdir()
    (directory / "rounds").mkdir()
    write_json(directory / "input-manifest.json", {
        "prepared_at": now(), "snapshot_manifest_sha256": digest(manifest_path),
        "files": records, "instructions_sha256": digest(workspace / "AGENTS.md"),
    })
    write_json(directory / "state.json", {
        "run": run, "status": "prepared", "settings": SETTINGS,
        "workspace": str(workspace), "thread_id": None, "rounds": [],
    })
    print(json.dumps({"run": run, "workspace": str(workspace), "inputs": len(records)}))


def command(codex, thread_id, final):
    argv = [codex, "exec", "--approve-for-me", "-m", SETTINGS["model"],
            "-c", 'model_reasoning_effort="high"',
            "-c", 'sandbox_mode="workspace-write"',
            "-c", "sandbox_workspace_write.network_access=true"]
    if thread_id:
        argv.extend(["resume", thread_id])
    argv.extend(["--skip-git-repo-check", "--json", "-o", str(final), "-"])
    return argv


def collect_event(event, state, record, directory):
    kind = event.get("type")
    if kind == "thread.started":
        thread_id = event["thread_id"]
        if state["thread_id"] and state["thread_id"] != thread_id:
            raise ValueError("Resume started an unexpected conversation")
        state["thread_id"] = thread_id
        record["thread_id"] = thread_id
        write_json(directory / "state.json", state)
    elif kind == "turn.completed":
        record["turn_completed"] = True
        record["usage"] = event.get("usage")
    elif kind == "turn.failed":
        record["turn_failed"] = True
        record.setdefault("errors", []).append(event.get("error"))
    elif kind == "error":
        record.setdefault("errors", []).append(event)
    elif kind == "item.completed":
        item = event.get("item", {})
        if item.get("type") == "command_execution":
            exit_code = item.get("exit_code")
            if exit_code not in (None, 0) or item.get("status") == "failed":
                record["command_failures"].append({
                    "id": item.get("id"), "command": item.get("command"),
                    "exit_code": exit_code, "status": item.get("status"),
                })


def copy_outputs(workspace, destination):
    shutil.copytree(workspace / "outputs", destination)
    return [{"path": str(path.relative_to(destination)), "sha256": digest(path),
             "size_bytes": path.stat().st_size} for path in files_under(destination)]


def turn(run, round_name, prompt_path, codex):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", round_name):
        raise ValueError("Round names must be simple immutable directory names")
    directory = run_path(run)
    state = json.loads((directory / "state.json").read_text())
    workspace = Path(state["workspace"])
    if state["status"] == "running":
        raise ValueError("This run already has an active round; inspect its process first")
    inputs = json.loads((directory / "input-manifest.json").read_text())
    validate_inputs(workspace, inputs["files"])
    if digest(workspace / "AGENTS.md") != inputs["instructions_sha256"]:
        raise ValueError("Workspace instructions changed")
    prompt = prompt_path.read_text()
    if not prompt.strip():
        raise ValueError("A confirmed nonempty prompt is required")
    round_directory = directory / "rounds" / round_name
    round_directory.mkdir()
    (round_directory / "prompt.txt").write_text(prompt)
    before = copy_outputs(workspace, round_directory / "before")
    argv = command(codex, state["thread_id"], round_directory / "final.txt")
    record = {"round": round_name, "started_at": now(), "status": "running",
              "argv": argv, "cwd": str(workspace), "settings": SETTINGS,
              "mode": "resume" if state["thread_id"] else "new_session",
              "thread_id": state["thread_id"], "prompt_sha256": digest(round_directory / "prompt.txt"),
              "before_outputs": before, "turn_completed": False, "turn_failed": False,
              "command_failures": [], "exit_code": None}
    state["status"] = "running"
    state["rounds"].append(round_name)
    write_json(directory / "state.json", state)
    write_json(round_directory / "execution.json", record)
    process = None
    try:
        with (round_directory / "events.jsonl").open("w") as events, \
                (round_directory / "stderr.log").open("w") as errors, \
                (round_directory / "prompt.txt").open("r") as prompt_input:
            process = subprocess.Popen(argv, cwd=workspace, stdin=prompt_input,
                                       stdout=subprocess.PIPE, stderr=errors, text=True,
                                       encoding="utf-8")
            record["process_id"] = process.pid
            write_json(round_directory / "execution.json", record)
            for line in process.stdout:
                events.write(line)
                events.flush()
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    record.setdefault("unparsed_event_lines", []).append(line.rstrip())
                    continue
                collect_event(event, state, record, directory)
                write_json(round_directory / "execution.json", record)
            record["exit_code"] = process.wait()
    except Exception as error:
        record.setdefault("runner_errors", []).append(str(error))
        if process is not None and process.poll() is None:
            process.terminate()
            record["exit_code"] = process.wait()
    finally:
        if process is not None and process.stdout is not None:
            process.stdout.close()
    record["after_outputs"] = copy_outputs(workspace, round_directory / "after")
    try:
        validate_inputs(workspace, inputs["files"])
        if digest(workspace / "AGENTS.md") != inputs["instructions_sha256"]:
            raise ValueError("Workspace instructions changed during the round")
        record["inputs_unchanged"] = True
    except ValueError as error:
        record["inputs_unchanged"] = False
        record.setdefault("runner_errors", []).append(str(error))
    final = round_directory / "final.txt"
    record["final_saved"] = final.is_file() and bool(final.read_text().strip())
    complete = (record["exit_code"] == 0 and record["turn_completed"]
                and not record["turn_failed"] and not record.get("runner_errors")
                and bool(state["thread_id"]) and record["final_saved"])
    record["status"] = "completed" if complete else "incomplete"
    record["finished_at"] = now()
    state["status"] = record["status"]
    state["thread_id"] = record["thread_id"]
    write_json(round_directory / "execution.json", record)
    write_json(directory / "state.json", state)
    print(json.dumps({"run": run, "round": round_name, "status": record["status"],
                      "thread_id": state["thread_id"], "exit_code": record["exit_code"],
                      "command_failures": len(record["command_failures"])}))
    return 0 if complete else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("freeze")
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--run", type=int, choices=(1, 2, 3), required=True)
    prepare_parser.add_argument("--corpus", type=Path, required=True)
    turn_parser = subparsers.add_parser("turn")
    turn_parser.add_argument("--run", type=int, choices=(1, 2, 3), required=True)
    turn_parser.add_argument("--round", required=True)
    turn_parser.add_argument("--prompt", type=Path, required=True)
    turn_parser.add_argument("--codex", default="codex")
    args = parser.parse_args()
    if args.action == "freeze":
        freeze()
    elif args.action == "prepare":
        prepare(args.run, args.corpus)
    else:
        return turn(args.run, args.round, args.prompt, args.codex)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        print(f"Runner stopped: {error}", file=sys.stderr)
        sys.exit(1)
