#!/usr/bin/env python3
"""Portable ZIP selection, closure, and atomic replacement regressions."""
from __future__ import annotations

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import package_release as package  # noqa: E402


class PackageReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        for relative in package.RUNTIME_FILES:
            self.write(relative, b"fixture\n")
        self.write("SKILL.md", b"---\nname: survey-orchestrator\ndescription: fixture\n---\n[Guide](references/guide.md)\n")
        self.write("references/guide.md", b"[Root](../SKILL.md)\n")
        self.write("assets/survey-slide-templates.html", b'<img src="miru-reference-excerpts/sample.png"><a href="../references/guide.md">guide</a>')
        self.write("assets/miru-reference-excerpts/sample.png", b"image")
        upstream = Path(self.temporary.name) / "upstream"
        upstream.mkdir()
        self.git(upstream, "init", "-q")
        for relative in package.FONT_FILES:
            target = upstream / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"font fixture\n")
        (upstream / "SKILL.md").write_text(
            "---\nname: japanese-font-rendering\ndescription: font fixture\n---\n"
            "# Font guide\n[Context](references/contexts.md)\n[Log](references/knowledge-log.md)\n",
            encoding="utf-8",
        )
        self.git(upstream, "add", ".")
        self.git(upstream, "commit", "-qm", "font fixture")
        self.git(self.root, "init", "-q")
        self.git(self.root, "submodule", "add", "-q", str(upstream), package.FONT_SKILL)
        self.write("references/font.md", f"[Font](../{package.FONT_SKILL}/SKILL.md)\n".encode())
        self.output = Path(self.temporary.name) / "release.zip"

    def git(self, directory: Path, *arguments: str) -> str:
        result = subprocess.run([
            "git", "-c", "protocol.file.allow=always", "-c", "user.name=Packaging Tests",
            "-c", "user.email=packaging-tests@example.invalid", "-c", "commit.gpgsign=false",
            "-C", str(directory), *arguments,
        ], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def write(self, relative: str, content: bytes) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def test_untracked_source_and_both_layouts(self) -> None:
        for unwanted in (
            "evaluations/case/source.pdf", "tmp/source.pdf", "corpus/data.json",
            "tests/test_private.py", "scripts/__pycache__/module.pyc", "scripts/unknown.py",
            "references/.env", "references/cache/old.md", "assets/.secret.json",
        ):
            self.write(unwanted, b"excluded")
        expected = set(package.RUNTIME_FILES) | {
            "references/guide.md", "references/font.md", "assets/miru-reference-excerpts/sample.png",
            f"{package.FONT_SKILL}/GUIDE.md", f"{package.FONT_SKILL}/references/contexts.md",
            f"{package.FONT_SKILL}/references/knowledge-log.md", f"{package.FONT_SKILL}/assets/icon.svg",
            f"{package.FONT_SKILL}/provenance.json",
        }
        for layout in ("folder", "flat"):
            with self.subTest(layout=layout):
                package.build_archive(self.root, self.output, layout)
                with zipfile.ZipFile(self.output) as archive:
                    prefix = f"{package.ARCHIVE_ROOT}/" if layout == "folder" else ""
                    self.assertEqual(set(archive.namelist()), {prefix + name for name in expected})
                    self.assertIsNone(archive.testzip())
                    script = archive.getinfo(prefix + "scripts/setup_python_env.sh")
                    self.assertTrue((script.external_attr >> 16) & 0o111)
                    guide = archive.read(prefix + f"{package.FONT_SKILL}/GUIDE.md").decode()
                    self.assertTrue(guide.startswith("# Font guide"))
                    self.assertNotIn("name: japanese-font-rendering", guide)
                    self.assertIn("GUIDE.md", archive.read(prefix + "references/font.md").decode())
                    metadata = json.loads(archive.read(prefix + f"{package.FONT_SKILL}/provenance.json"))
                    self.assertEqual(metadata["revision"], self.git(self.root / package.FONT_SKILL, "rev-parse", "HEAD"))
                    for entry in archive.namelist():
                        self.assertNotIn(self.temporary.name.encode(), archive.read(entry))
                        self.assertNotIn(b"/Users/", archive.read(entry))

    def test_identical_sources_produce_identical_archives(self) -> None:
        package.build_archive(self.root, self.output)
        original = self.output.read_bytes()
        package.build_archive(self.root, self.output)
        self.assertEqual(original, self.output.read_bytes())

    def test_missing_runtime_file_preserves_existing_archive(self) -> None:
        self.output.write_bytes(b"existing archive")
        (self.root / "devbox.lock").unlink()
        with self.assertRaisesRegex(package.PackageError, "required runtime file"):
            package.build_archive(self.root, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing archive")

    def test_markdown_and_html_missing_targets_fail(self) -> None:
        cases = {
            "references/guide.md": b"[Unbundled evaluation](../evaluations/case/report.md)",
            "assets/survey-slide-templates.html": b'<img src="missing.png">',
        }
        for source, content in cases.items():
            with self.subTest(source=source):
                original = (self.root / source).read_bytes()
                self.write(source, content)
                with self.assertRaisesRegex(package.PackageError, "local link is not bundled"):
                    package.build_archive(self.root, self.output)
                self.write(source, original)

    def test_escaping_link_and_nested_entrypoint_fail(self) -> None:
        self.write("references/guide.md", b"[Escape](../../outside.md)")
        with self.assertRaisesRegex(package.PackageError, "escapes the bundle"):
            package.build_archive(self.root, self.output)
        self.write("references/guide.md", b"guide")
        self.write("references/SKILL.md", b"unexpected entrypoint")
        with self.assertRaisesRegex(package.PackageError, "exactly one root"):
            package.build_archive(self.root, self.output)

    def test_symlink_source_and_runtime_output_fail(self) -> None:
        guide = self.root / "references/guide.md"
        guide.unlink()
        guide.symlink_to(self.root / "SKILL.md")
        with self.assertRaisesRegex(package.PackageError, "symlink"):
            package.build_archive(self.root, self.output)
        guide.unlink()
        guide.write_text("guide", encoding="utf-8")
        with self.assertRaisesRegex(package.PackageError, "runtime directory"):
            package.build_archive(self.root, self.root / "assets/release.zip")

    def test_zip_write_failure_keeps_output_and_removes_temporary_file(self) -> None:
        self.output.write_bytes(b"existing archive")
        with mock.patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("simulated failure")):
            with self.assertRaisesRegex(OSError, "simulated failure"):
                package.build_archive(self.root, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing archive")
        self.assertEqual(list(self.output.parent.glob(".release.zip.*.tmp")), [])

    def test_missing_font_submodule_preserves_existing_archive(self) -> None:
        self.output.write_bytes(b"existing archive")
        shutil.rmtree(self.root / package.FONT_SKILL)
        with self.assertRaisesRegex(package.PackageError, "not initialized"):
            package.build_archive(self.root, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing archive")

    def test_dirty_font_submodule_is_rejected(self) -> None:
        self.write(f"{package.FONT_SKILL}/references/contexts.md", b"uncommitted recipe")
        with self.assertRaisesRegex(package.PackageError, "submodule is dirty"):
            package.build_archive(self.root, self.output)

    def test_untracked_font_file_is_rejected(self) -> None:
        self.write(f"{package.FONT_SKILL}/private.txt", b"not a committed source")
        with self.assertRaisesRegex(package.PackageError, "submodule is dirty"):
            package.build_archive(self.root, self.output)

    def test_font_pin_mismatch_is_rejected(self) -> None:
        dependency = self.root / package.FONT_SKILL
        self.write(f"{package.FONT_SKILL}/references/contexts.md", b"new committed recipe")
        self.git(dependency, "add", ".")
        self.git(dependency, "commit", "-qm", "new font revision")
        with self.assertRaisesRegex(package.PackageError, "pin mismatch"):
            package.build_archive(self.root, self.output)


if __name__ == "__main__":
    unittest.main()
