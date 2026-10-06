#!/usr/bin/env python3
"""Regression cases for the deck observer's contract joins."""

from __future__ import annotations

import json
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import check_deck_quality as deck  # noqa: E402


def row() -> dict[str, str]:
    return {
        "slide_id": "slide-1",
        "plot_version": "v0.1",
        "plot_row_id": "P-01",
        "section_id": "SEC-01",
        "evidence_block_id": "EB-01",
        "visual_id": "V-1",
        "kind": "table",
        "claim_bearing": "true",
        "contract_path": "contracts/V-1.json",
        "claim_ids": "C-1",
        "source_visual_route": "no_useful_candidate",
        "reader_role": "claim comparison",
        "boundary": "observed sample only",
        "status": "SURVEY-SYNTHESIS",
        "semantic_status": "passed",
        "fidelity_status": "not_required",
        "visual_review_status": "not_required",
    }


def contract() -> dict:
    return {
        "visual_id": "V-1",
        "slide_id": "slide-1",
        "kind": "table",
        "claim_bearing": True,
        "source_visual_route": "no_useful_candidate",
        "reader_role": "claim comparison",
        "boundary": "observed sample only",
        "status": "SURVEY-SYNTHESIS",
        "semantic_status": "passed",
        "fidelity_status": "not_required",
        "visual_review_status": "not_required",
        "review": {
            "deterministic_status": "passed",
            "semantic_status": "passed",
            "fidelity_status": "not_required",
        },
    }


class DeckContractLinkTests(unittest.TestCase):
    def test_matching_contract_is_observed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            (root / "contracts" / "V-1.json").write_text(json.dumps(contract()), encoding="utf-8")
            errors, warnings = deck.check_visual_contract_links([row()], root, True)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_route_kind_and_status_mismatch_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "contracts").mkdir()
            bad = contract()
            bad.update({"kind": "chart", "source_visual_route": "inaccessible_source", "semantic_status": "blocked"})
            (root / "contracts" / "V-1.json").write_text(json.dumps(bad), encoding="utf-8")
            errors, _warnings = deck.check_visual_contract_links([row()], root, True)
            self.assertTrue(errors)

    def test_missing_or_outside_contract_is_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_row = row()
            manifest_row["contract_path"] = "../outside.json"
            errors, _warnings = deck.check_visual_contract_links([manifest_row], root, True)
            self.assertTrue(any("outside" in error or "local" in error for error in errors))

    def test_missing_claim_bearing_is_not_skipped_when_contract_columns_exist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_row = row()
            manifest_row.pop("claim_bearing")
            manifest_row["claim_ids"] = ""
            manifest_row["contract_path"] = ""
            errors, _warnings = deck.check_visual_contract_links([manifest_row], root, True)
            self.assertTrue(any("claim_bearing" in error for error in errors))

    def test_external_source_cutout_output_is_not_hashed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = root / "records"
            records.mkdir()
            outside = root.parent / f"outside-source-cutout-{root.name}.bin"
            outside.write_bytes(b"must not be read")
            try:
                (records / "cutout.json").write_text(json.dumps({
                    "asset_id": "A-1",
                    "visual_id": "V-1",
                    "asset_role": "source_cutout",
                    "review_only": True,
                    "figure_id": "F-1",
                    "rights_basis": "article32_quotation",
                    "fidelity_status": "passed",
                    "source_id": "S-1",
                    "claim_ids": ["C-1"],
                    "source_sha256": "a" * 64,
                    "output_sha256": "b" * 64,
                    "source_hash_basis": "local_source_file",
                    "output": str(outside),
                }), encoding="utf-8")
                manifest_row = {
                    "slide_id": "slide-1",
                    "visual_id": "V-1",
                    "figure_id": "F-1",
                    "source_ids": "S-1",
                    "claim_ids": "C-1",
                    "source_cutout_asset_ids": "A-1",
                    "source_cutout_manifest_paths": "records/cutout.json",
                    "rights_basis": "article32_quotation",
                    "fidelity_status": "passed",
                }
                with mock.patch.object(deck, "sha256_file", side_effect=AssertionError("external file was hashed")):
                    errors, _warnings, _records = deck.check_source_cutout_records(
                        manifest_row, ["A-1"], ["records/cutout.json"], root, True
                    )
                self.assertTrue(any("outside audit-root" in error for error in errors))
            finally:
                outside.unlink(missing_ok=True)

    def test_referenced_records_without_audit_root_are_errors_even_non_strict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row_data = row()
            row_data.update({
                "source_scan_record_paths": "records/scan.json",
                "source_visual_route": "no_useful_candidate",
            })
            errors, warnings, _records = deck.check_scan_records(row_data, None, False)
            self.assertTrue(errors)
            self.assertEqual(warnings, [])
            self.assertIn("--audit-root", errors[0])

    def test_cli_does_not_infer_audit_root_from_manifest_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_row = row()
            manifest_row.update({
                "narrative_job": "evidence",
                "evidence_class": "evidence",
                "primary_visual_type": "result_table",
                "source_pointer": "S-1",
                "citation_visible": "true",
                "numeric": "false",
                "denominator_unit": "not measured",
                "aggregation_level": "study",
                "caveat_visible": "true",
                "min_body_pt": "16",
                "protected_terms": "",
                "internal_vocab_free": "true",
                "source_scan_record_paths": str(root.parent / "outside-scan.json"),
            })
            manifest_path = root / "manifest.tsv"
            with manifest_path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(manifest_row), delimiter="\t")
                writer.writeheader()
                writer.writerow(manifest_row)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "check_deck_quality.py"),
                    "--manifest",
                    str(manifest_path),
                    "--pdf",
                    str(root / "missing.pdf"),
                    "--strict",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            report = json.loads(proc.stdout)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", proc.stderr)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(any("--audit-root" in error for error in report["failures"]))


if __name__ == "__main__":
    unittest.main()
