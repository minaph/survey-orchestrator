#!/usr/bin/env python3
"""Tests for the formal storyline-plot joins."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from check_storyline_plot import check_plot_payload  # noqa: E402


def payload() -> dict:
    return {
        "plot_version": "v0.1",
        "plot_scope": "target_survey",
        "plot_status": "verified",
        "rows": [{
            "plot_row_id": "P-01",
            "section_id": "SEC-01",
            "evidence_block_id": "EB-01",
            "slide_id": "slide-1",
            "T": "Question",
            "B": "Basis",
            "Bottom": "Boundary-qualified answer",
            "Figure": "Comparison relation",
            "Next": "Next question",
            "claim_ids": ["C-1"],
            "source_ids": ["S-1"],
            "visual_ids": ["V-1"],
        }],
    }


def manifest() -> list[dict[str, str]]:
    return [{
        "slide_id": "slide-1",
        "plot_version": "v0.1",
        "plot_row_id": "P-01",
        "section_id": "SEC-01",
        "evidence_block_id": "EB-01",
        "visual_id": "V-1",
        "claim_ids": "C-1",
        "source_ids": "S-1",
    }]


class StorylinePlotTests(unittest.TestCase):
    def test_strict_plot_manifest_chain_passes(self) -> None:
        errors, warnings, metrics = check_plot_payload(payload(), manifest(), strict=True)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(metrics["joined_manifest_rows"], 1)

    def test_plot_row_id_is_the_stable_join_key(self) -> None:
        changed = manifest()
        changed[0]["slide_id"] = "slide-9"
        errors, _warnings, _metrics = check_plot_payload(payload(), changed, strict=True)
        self.assertTrue(any("slide_id" in error for error in errors))

    def test_missing_reader_loop_field_is_formal_failure_at_release(self) -> None:
        changed = payload()
        changed["rows"][0].pop("Figure")
        errors, _warnings, _metrics = check_plot_payload(changed, manifest(), strict=True)
        self.assertTrue(any("missing Figure" in error for error in errors))

    def test_one_evidence_block_may_span_multiple_plot_rows(self) -> None:
        changed = payload()
        second = dict(changed["rows"][0])
        second.update({"plot_row_id": "P-02", "slide_id": "slide-2", "visual_ids": ["V-2"]})
        changed["rows"].append(second)
        rows = manifest() + [{
            "slide_id": "slide-2",
            "plot_version": "v0.1",
            "plot_row_id": "P-02",
            "section_id": "SEC-01",
            "evidence_block_id": "EB-01",
            "visual_id": "V-2",
            "claim_ids": "C-1",
            "source_ids": "S-1",
        }]
        errors, _warnings, _metrics = check_plot_payload(changed, rows, strict=True)
        self.assertFalse(any("assigned to multiple" in error for error in errors))

    def test_plot_scope_is_not_silently_defaulted(self) -> None:
        changed = payload()
        changed.pop("plot_scope")
        errors, _warnings, _metrics = check_plot_payload(changed, manifest(), strict=True)
        self.assertTrue(any("plot_scope" in error for error in errors))

    def test_non_object_plot_row_is_not_dropped(self) -> None:
        changed = payload()
        changed["rows"].append("malformed")
        errors, _warnings, _metrics = check_plot_payload(changed, manifest(), strict=True)
        self.assertTrue(any("non-object" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
