#!/usr/bin/env python3
"""Build an atomic runtime-only skill ZIP, including untracked source files."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile


ARCHIVE_ROOT = "survey-orchestrator"
RUNTIME_FILES = (
    "SKILL.md", "agents/openai.yaml", "devbox.json", "devbox.lock", "requirements.txt",
    "scripts/check_deck_quality.py", "scripts/check_evidence_visual_contract.py",
    "scripts/check_review_record.py", "scripts/check_storyline_plot.py",
    "scripts/extract_source_figure.py", "scripts/manifest_visuals.py",
    "scripts/setup_python_env.sh", "scripts/check_evaluation_environment.py",
    "scripts/package_release.py", "assets/icon.svg", "assets/survey-slide-templates.html",
    "assets/miru-reference-excerpts/provenance.json",
)
RUNTIME_TREES = {
    "references": {".md"},
    "assets/miru-reference-excerpts": {".png"},
}
EXCLUDED_PARTS = {"__pycache__", "cache", "tmp", "evaluations", "corpus", "logs"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FONT_SKILL = "skills/japanese-font-rendering"
FONT_FILES = ("SKILL.md", "references/contexts.md", "references/knowledge-log.md", "assets/icon.svg")
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)


class PackageError(ValueError):
    """The source cannot produce a complete and safe runtime bundle."""


class HTMLLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append(value)


def _read_runtime_file(root: Path, relative: str) -> bytes:
    source = root / relative
    for parent in [source, *source.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise PackageError(f"runtime path cannot be a symlink: {relative}")
    if not source.is_file() or not source.resolve().is_relative_to(root):
        raise PackageError(f"required runtime file is missing or unsafe: {relative}")
    return source.read_bytes()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if result.returncode:
        raise PackageError(f"Git inspection failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _bundle_font_skill(root: Path, files: dict[str, bytes]) -> None:
    dependency = root / FONT_SKILL
    if dependency.is_symlink() or not (dependency / ".git").is_file():
        raise PackageError(f"font submodule is not initialized: {FONT_SKILL}")
    entries = _git(root, "ls-files", "--stage", "--", FONT_SKILL).splitlines()
    if len(entries) != 1:
        raise PackageError(f"font dependency is not a pinned submodule: {FONT_SKILL}")
    metadata, path = entries[0].split("\t", 1)
    mode, revision, stage = metadata.split()
    if mode != "160000" or stage != "0" or path != FONT_SKILL:
        raise PackageError(f"font dependency is not a pinned submodule: {FONT_SKILL}")
    if Path(_git(dependency, "rev-parse", "--show-toplevel")).resolve() != dependency.resolve():
        raise PackageError(f"font submodule is not initialized: {FONT_SKILL}")
    if _git(dependency, "rev-parse", "HEAD") != revision:
        raise PackageError(f"font submodule pin mismatch: {FONT_SKILL}")
    if _git(dependency, "status", "--porcelain", "--untracked-files=all"):
        raise PackageError(f"font submodule is dirty: {FONT_SKILL}")
    reference_files = {
        path for path in _git(dependency, "ls-files", "-z", "--", "references").split("\0")
        if path and PurePosixPath(path).suffix in {".md", ".yaml", ".json"}
    }
    for relative in sorted(set(FONT_FILES) | reference_files):
        content = _read_runtime_file(root, f"{FONT_SKILL}/{relative}")
        destination = f"{FONT_SKILL}/{relative}"
        if relative == "SKILL.md":
            text = content.decode("utf-8")
            match = FRONTMATTER.match(text)
            if not match:
                raise PackageError("font skill has no YAML frontmatter")
            content = text[match.end():].encode("utf-8")
            destination = f"{FONT_SKILL}/GUIDE.md"
        files[destination] = content
    files[f"{FONT_SKILL}/provenance.json"] = (json.dumps({
        "repository": "https://github.com/minaph/japanese-font-rendering",
        "revision": revision,
        "entrypoint": "GUIDE.md",
        "transformation": "SKILL.md renamed; YAML frontmatter removed; body preserved",
    }, indent=2) + "\n").encode("utf-8")
    for path, content in files.items():
        if PurePosixPath(path).suffix == ".md":
            files[path] = content.replace(f"{FONT_SKILL}/SKILL.md".encode(), f"{FONT_SKILL}/GUIDE.md".encode())


def collect_runtime_files(root: Path) -> dict[str, bytes]:
    """Allowlist parent files and verify the Git pin of the font dependency."""
    root = root.resolve()
    files = {path: _read_runtime_file(root, path) for path in RUNTIME_FILES}
    for directory, extensions in RUNTIME_TREES.items():
        tree = root / directory
        if tree.is_symlink() or not tree.is_dir():
            raise PackageError(f"runtime directory is missing or unsafe: {directory}")
        for source in sorted(tree.rglob("*")):
            relative = source.relative_to(root)
            if any(part.startswith(".") or part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if source.is_symlink():
                raise PackageError(f"runtime path cannot be a symlink: {relative}")
            if source.is_file() and source.suffix in extensions:
                files[relative.as_posix()] = _read_runtime_file(root, relative.as_posix())
    _bundle_font_skill(root, files)
    validate_runtime_files(files)
    return files


def _validate_link(source: str, destination: str, available: set[str]) -> None:
    try:
        url = urlsplit(destination)
    except ValueError as error:
        raise PackageError(f"invalid link: {source} -> {destination}") from error
    if url.scheme == "file":
        raise PackageError(f"local file URI is not portable: {source} -> {destination}")
    if url.scheme or url.netloc or not url.path:
        return
    target = PurePosixPath(unquote(url.path))
    if target.is_absolute():
        raise PackageError(f"absolute local link is not portable: {source} -> {destination}")
    parts = list(PurePosixPath(source).parent.parts)
    for part in target.parts:
        if part == "..":
            if not parts:
                raise PackageError(f"local link escapes the bundle: {source} -> {destination}")
            parts.pop()
        elif part != ".":
            parts.append(part)
    if PurePosixPath(*parts).as_posix() not in available:
        raise PackageError(f"local link is not bundled: {source} -> {destination}")


def validate_runtime_files(files: dict[str, bytes]) -> None:
    skill_paths = [path for path in files if PurePosixPath(path).name == "SKILL.md"]
    if skill_paths != ["SKILL.md"]:
        raise PackageError("bundle must contain exactly one root SKILL.md")
    for path, content in files.items():
        suffix = PurePosixPath(path).suffix
        if suffix not in {".md", ".html"}:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise PackageError(f"runtime text is not UTF-8: {path}") from error
        if suffix == ".md":
            links = []
            for destination in MARKDOWN_LINK.findall(text):
                destination = destination.strip()
                if not destination:
                    continue
                if destination.startswith("<"):
                    if ">" not in destination:
                        raise PackageError(f"invalid Markdown link in {path}: {destination}")
                    destination = destination[1:destination.index(">")]
                else:
                    destination = destination.split(maxsplit=1)[0]
                links.append(destination)
        else:
            parser = HTMLLinks()
            parser.feed(text)
            links = parser.links
        for destination in links:
            _validate_link(path, destination, set(files))


def build_archive(root: Path, output: Path, layout: str = "folder") -> Path:
    """Validate everything before replacing an existing archive."""
    if layout not in {"folder", "flat"}:
        raise PackageError(f"unsupported archive layout: {layout}")
    root = root.resolve()
    if output.is_symlink():
        raise PackageError(f"archive output cannot be a symlink: {output}")
    output = output.resolve()
    if output.suffix.lower() != ".zip" or output.is_dir():
        raise PackageError(f"archive output must be a .zip file: {output}")
    if output.is_relative_to(root):
        relative = output.relative_to(root)
        if relative.parts[0] in {".git", "references", "scripts", "assets", "agents", "skills"}:
            raise PackageError(f"archive output cannot overwrite a runtime directory: {output}")
    files = collect_runtime_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(dir=output.parent, prefix=f".{output.name}.", suffix=".tmp")
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path, content in sorted(files.items()):
                name = f"{ARCHIVE_ROOT}/{path}" if layout == "folder" else path
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = (0o100755 if path.endswith(".sh") else 0o100644) << 16
                archive.writestr(entry, content)
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise PackageError("archive integrity check failed")
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return output


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist") / f"{ARCHIVE_ROOT}.zip")
    parser.add_argument("--layout", choices=("folder", "flat"), default="folder")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        print(f"Created {build_archive(root, output, args.layout)}")
    except (PackageError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
