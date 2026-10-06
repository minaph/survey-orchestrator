import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("plot_runner", Path(__file__).with_name("runner.py"))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

FAKE_CODEX = '''#!/usr/bin/env python3
import json
from pathlib import Path
import sys

prompt = sys.stdin.read()
argv = sys.argv[1:]
final = Path(argv[argv.index("-o") + 1])
thread = "a1111111-2222-4333-8444-555555555555"
if "resume" in argv:
    assert argv[argv.index("resume") + 1] == thread
assert "--approve-for-me" in argv
assert "--sandbox" not in argv
assert "--ephemeral" not in argv
assert "--profile" not in argv
assert "gpt-6-luna" in argv
print(json.dumps({"type": "thread.started", "thread_id": thread}), flush=True)
(Path("outputs") / "plot.md").write_text(prompt)
final.write_text("Final response for: " + prompt)
if "command_failure" in prompt:
    print(json.dumps({"type": "item.completed", "item": {
        "id": "check-1", "type": "command_execution", "command": "false", "exit_code": 1, "status": "failed"}}))
if "turn_failure" in prompt:
    print(json.dumps({"type": "turn.failed", "error": {"message": "fake failure"}}))
else:
    print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}}))
'''


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="plot-runner-test-")
        self.root = Path(self.temporary.name)
        self.previous_root = runner.REPOSITORY_ROOT
        self.previous_evaluation = runner.EVALUATION_ROOT
        runner.REPOSITORY_ROOT = self.root / "repository"
        runner.EVALUATION_ROOT = runner.REPOSITORY_ROOT / "evaluations/luna-plot-study"
        (runner.EVALUATION_ROOT / "runtime").mkdir(parents=True)
        (runner.REPOSITORY_ROOT / "SKILL.md").write_text("frozen skill")
        for name in runner.SKILL_ROOTS[1:]:
            directory = runner.REPOSITORY_ROOT / name
            directory.mkdir()
            (directory / "fixture.txt").write_text(name)
        self.corpus = self.root / "corpus"
        self.corpus.mkdir()
        (self.corpus / "paper.pdf").write_bytes(b"mock paper bytes")
        self.fake = self.root / "fake-codex"
        self.fake.write_text(FAKE_CODEX)
        self.fake.chmod(0o755)

    def tearDown(self):
        runner.REPOSITORY_ROOT = self.previous_root
        runner.EVALUATION_ROOT = self.previous_evaluation
        self.temporary.cleanup()

    def prompt(self, text, name="prompt.txt"):
        path = self.root / name
        path.write_text(text)
        return path

    def prepared(self):
        runner.freeze()
        runner.prepare(1, self.corpus)

    def test_three_identical_copies_and_immutable_preparation(self):
        runner.freeze()
        for number in (1, 2, 3):
            runner.prepare(number, self.corpus)
        manifests = [json.loads((runner.run_path(number) / "input-manifest.json").read_text())
                     for number in (1, 2, 3)]
        self.assertEqual(manifests[0]["files"], manifests[1]["files"])
        self.assertEqual(manifests[1]["files"], manifests[2]["files"])
        with self.assertRaises(ValueError):
            runner.freeze()
        with self.assertRaises(ValueError):
            runner.prepare(1, self.corpus)

    def test_resume_preserves_initial_and_before_after_outputs(self):
        self.prepared()
        self.assertEqual(runner.turn(1, "draft", self.prompt("first plot"), str(self.fake)), 0)
        self.assertEqual(runner.turn(1, "r1", self.prompt("second plot", "r1.txt"), str(self.fake)), 0)
        rounds = runner.run_path(1) / "rounds"
        self.assertEqual((rounds / "draft/after/plot.md").read_text(), "first plot")
        self.assertEqual((rounds / "r1/before/plot.md").read_text(), "first plot")
        self.assertEqual((rounds / "r1/after/plot.md").read_text(), "second plot")
        record = json.loads((rounds / "r1/execution.json").read_text())
        self.assertEqual(record["mode"], "resume")
        self.assertEqual(record["thread_id"], "a1111111-2222-4333-8444-555555555555")
        self.assertTrue(record["inputs_unchanged"])
        with self.assertRaises(FileExistsError):
            runner.turn(1, "draft", self.prompt("do not replace"), str(self.fake))

    def test_failed_internal_command_is_retained_separately(self):
        self.prepared()
        self.assertEqual(runner.turn(1, "draft", self.prompt("command_failure"), str(self.fake)), 0)
        record = json.loads((runner.run_path(1) / "rounds/draft/execution.json").read_text())
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["command_failures"][0]["exit_code"], 1)

    def test_exit_zero_without_successful_turn_is_incomplete(self):
        self.prepared()
        self.assertEqual(runner.turn(1, "draft", self.prompt("turn_failure"), str(self.fake)), 1)
        record = json.loads((runner.run_path(1) / "rounds/draft/execution.json").read_text())
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["status"], "incomplete")

    def test_modified_frozen_input_blocks_launch(self):
        self.prepared()
        (runner.run_path(1) / "workspace/SKILL.md").write_text("changed skill")
        with self.assertRaisesRegex(ValueError, "Frozen input changed"):
            runner.turn(1, "draft", self.prompt("must not launch"), str(self.fake))
        self.assertFalse((runner.run_path(1) / "rounds/draft").exists())


if __name__ == "__main__":
    unittest.main()
