#!/usr/bin/env python3
"""Tests for the formal plot/reader review record."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from check_review_record import check_review_payload  # noqa: E402


PLOT_ROWS = [{"plot_row_id": "P-01"}]
MANIFEST_ROWS = [{"slide_id": "slide-1", "visual_id": "V-01", "claim_ids": "C-01"}]


def review() -> dict:
    return {
        "plot_review": {
            "status": "passed",
            "plot_version": "v0.1",
            "scope": {"coverage": "all", "rows": ["P-01"], "pages": ["slide-1"]},
            "findings": [{
                "row": "P-01",
                "page": "slide-1",
                "question": "Does the story start clearly?",
                "verdict": "strong",
                "repair": "none",
                "recheck": "Read the opening after render.",
            }],
        },
        "reader_review": {
            "status": "passed",
            "scope": {"coverage": "all", "pages": ["slide-1"]},
            "score": 80,
            "denominator": 100,
            "findings": [],
        },
        "deterministic": {"status": "passed"},
        "semantic": {"status": "passed"},
        "fidelity": {"status": "not_required"},
        "visual_review": {"status": "passed"},
        "release": "passed",
    }


class ReviewRecordTests(unittest.TestCase):
    def test_strict_record_passes(self) -> None:
        errors, warnings, metrics = check_review_payload(
            review(), PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(metrics["plot_review_findings"], 1)

    def test_unresolved_plot_review_blocks_strict_release(self) -> None:
        changed = review()
        changed["plot_review"]["status"] = "blocked"
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertTrue(any("plot_review.status" in error for error in errors))

    def test_findings_need_repair_and_recheck_fields(self) -> None:
        changed = review()
        changed["plot_review"]["findings"][0].pop("recheck")
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertTrue(any("lacks recheck" in error for error in errors))

    def test_review_version_must_match_current_plot(self) -> None:
        errors, _warnings, _metrics = check_review_payload(
            review(), PLOT_ROWS, MANIFEST_ROWS, strict=True, expected_plot_version="v0.2"
        )
        self.assertTrue(any("plot_version" in error for error in errors))

    def test_finding_locator_must_stay_inside_declared_scope(self) -> None:
        changed = review()
        changed["plot_review"]["findings"][0]["page"] = "slide-9"
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertTrue(any("outside declared scope" in error for error in errors))

    def test_claim_or_visual_is_an_accepted_plot_finding_locator(self) -> None:
        changed = review()
        finding = changed["plot_review"]["findings"][0]
        finding.pop("row")
        finding["claim_or_visual"] = "V-01"
        changed["plot_review"]["scope"]["items"] = ["V-01"]
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertEqual(errors, [])

    def test_unknown_reader_claim_or_visual_is_rejected(self) -> None:
        changed = review()
        changed["reader_review"]["scope"]["items"] = ["V-01"]
        changed["reader_review"]["findings"] = [{
            "claim_or_visual": "V-99",
            "page": "slide-1",
            "question": "Is the visual attributable?",
            "verdict": "adequate",
            "repair": "none",
            "recheck": "Read the credit after render.",
        }]
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertTrue(any("unknown claim/visual" in error for error in errors))

    def test_row_and_claim_or_visual_cannot_be_combined(self) -> None:
        changed = review()
        changed["plot_review"]["findings"][0]["claim_or_visual"] = "UNKNOWN"
        errors, _warnings, _metrics = check_review_payload(
            changed, PLOT_ROWS, MANIFEST_ROWS, strict=True
        )
        self.assertTrue(any("exactly one" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
