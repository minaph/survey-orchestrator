#!/usr/bin/env python3
"""Regression cases for the structured evidence-visual preflight."""

from __future__ import annotations

import json
import hashlib
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKER = SKILL_ROOT / "scripts" / "check_evidence_visual_contract.py"


def base_fixture(root: Path, *, kind: str = "table", route: str = "no_useful_candidate") -> None:
    (root / "contracts").mkdir()
    (root / "records").mkdir()
    manifest = {
        "visuals": [{
            "visual_id": "V-1",
            "slide_id": "slide-1",
            "plot_version": "v0.1",
            "plot_row_id": "P-01",
            "section_id": "SEC-01",
            "evidence_block_id": "EB-01",
            "kind": kind,
            "claim_bearing": True,
            "claim_ids": ["C-1"],
            "source_ids": [],
            "source_visual_route": route,
            "reader_role": "claim comparison",
            "boundary": "observed sample only",
            "status": "SURVEY-SYNTHESIS",
            "semantic_status": "passed",
            "fidelity_status": "not_required",
            "visual_review_status": "not_required",
            "contract_path": "contracts/V-1.json",
            "source_cutout_asset_ids": [],
            "source_cutout_manifest_paths": [],
            "source_scan_record_paths": [],
        }]
    }
    semantics = {
        "row_axis": {"name": "study", "meaning": "study being compared", "labels": ["A", "B"]},
        "column_axis": {"name": "condition", "meaning": "condition under which the result is reported", "labels": ["control", "task"]},
        "cell_meaning": "reported mean",
        "orientation": "rows=study; columns=condition",
        "axis_mirror": "rows = study being compared; columns = condition under which the result is reported; cell = reported mean; orientation = rows=study; columns=condition",
        "unit": "points",
        "cells": [[1, 2], [3, 4]],
    }
    if kind == "chart":
        semantics = {
            "x_axis": {"name": "condition", "unit": "category"},
            "y_axis": {"name": "score", "unit": "points"},
            "comparator": "control",
            "aggregation": "mean",
            "domain": {"type": "continuous", "min": 0, "max": 10},
        }
    contract = {
        "visual_id": "V-1",
        "slide_id": "slide-1",
        "kind": kind,
        "claim_ids": ["C-1"],
        "source_ids": [],
        "source_visual_route": route,
        "reader_role": "claim comparison",
        "boundary": "observed sample only",
        "status": "SURVEY-SYNTHESIS",
        "claim_bearing": True,
        "semantic_status": "passed",
        "review": {
            "deterministic_status": "passed",
            "semantic_status": "passed",
            "fidelity_status": "not_required",
        },
        "decision_reason_code": "no_source_figure",
        "source_cutout_asset_ids": [],
        "source_cutout_manifest_paths": [],
        "source_scan_record_paths": [],
        "semantics": semantics,
    }
    ledger = {"claims": [{"claim_id": "C-1"}], "sources": [], "assets": []}
    scan = {
        "record_type": "source_figure_scan",
        "visual_id": "V-1",
        "source_visual_route": "no_useful_candidate",
        "status": "no_candidate",
        "locator": "source text, results section",
        "reason": "No visual represents this claim.",
        "observed_at": "2026-08-10T09:00:00+09:00",
    }
    manifest_visual = manifest["visuals"][0]
    if route in {"no_useful_candidate", "faithful_reconstruction", "new_explanatory_visual"}:
        manifest_visual["source_scan_record_paths"] = ["records/scan.json"]
        contract["source_scan_record_paths"] = ["records/scan.json"]
        if route in {"no_useful_candidate", "faithful_reconstruction", "new_explanatory_visual"}:
            manifest_visual["decision_reason_code"] = "no_source_figure"
            contract["decision_reason_code"] = "no_source_figure"
    if route in {"faithful_reconstruction", "new_explanatory_visual"}:
        for record in (manifest_visual, contract):
            record.update({
                "derived_asset_id": "D-1",
                "derived_asset_path": "derived.txt",
                "visual_comparison_packet_path": "records/packet.json",
                "attribution_note": "Reconstructed by the survey",
                "reconstruction_created_at": "2026-08-10T09:01:00+09:00",
            })
    if route == "inaccessible_source":
        manifest_visual["source_ids"] = ["S-1"]
        manifest_visual["source_scan_record_paths"] = ["records/scan.json"]
        contract["source_ids"] = ["S-1"]
        contract["source_scan_record_paths"] = ["records/scan.json"]
        ledger["sources"] = [{"source_id": "S-1"}]
        scan = {
            "record_type": "source_figure_access",
            "visual_id": "V-1",
            "source_visual_route": "inaccessible_source",
            "status": "inaccessible",
            "access_status": "blocked",
            "locator": "publisher page",
            "observed_at": "2026-08-10T09:00:00+09:00",
        }
    if route == "source_figure":
        # This deliberate default gives the negative source_figure tests a
        # generic scan sidecar to reject. Valid source-figure tests replace it
        # with an explicit empty list and a cutout pair.
        manifest_visual["source_scan_record_paths"] = ["records/scan.json"]
        contract["source_scan_record_paths"] = ["records/scan.json"]
    for name, payload in (("manifest.json", manifest), ("ledger.json", ledger)):
        (root / name).write_text(json.dumps(payload), encoding="utf-8")
    (root / "contracts" / "V-1.json").write_text(json.dumps(contract), encoding="utf-8")
    (root / "records" / "scan.json").write_text(json.dumps(scan), encoding="utf-8")
    (root / "plot.json").write_text(json.dumps({
        "plot_version": "v0.1",
        "plot_scope": "target_survey",
        "plot_status": "verified",
        "rows": [{
            "plot_row_id": "P-01",
            "section_id": "SEC-01",
            "evidence_block_id": "EB-01",
            "slide_id": "slide-1",
            "T": "What is the comparison?",
            "B": "The evidence reports a bounded comparison.",
            "Bottom": "The result applies only to the observed sample.",
            "Figure": "The comparison relation is visible.",
            "Next": "What is the boundary of transfer?",
            "claim_ids": ["C-1"],
            "source_ids": [],
            "visual_ids": ["V-1"],
        }],
    }), encoding="utf-8")


def run_checker(
    root: Path,
    *,
    strict: bool = True,
    include_audit_root: bool = True,
    manifest_name: str = "manifest.json",
) -> tuple[dict, str, int]:
    command = [
        sys.executable,
        str(CHECKER),
        "--manifest", str(root / manifest_name),
        "--ledger", str(root / "ledger.json"),
        "--plot", str(root / "plot.json"),
    ]
    if include_audit_root:
        command.extend(["--audit-root", str(root)])
    if strict:
        command.append("--strict")
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    return json.loads(proc.stdout), proc.stderr, proc.returncode


class EvidenceVisualContractTests(unittest.TestCase):
    def test_valid_table_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(stderr, "")
            self.assertEqual(code, 0)

    def test_large_integer_does_not_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="chart")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["domain"]["max"] = 10 ** 4000
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertNotIn("Traceback", stderr)
            self.assertNotIn("OverflowError", stderr + json.dumps(report))
            self.assertEqual(report["status"], "pass")
            self.assertEqual(code, 0)

    def test_invalid_join_key_types_fail_without_stringification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["visual_id"] = ["V-1"]
            manifest["visuals"][0]["slide_id"] = True
            manifest_path.write_text(json.dumps(manifest))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_strict_without_audit_root_is_structured_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            report, stderr, code = run_checker(root, include_audit_root=False)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_non_strict_without_audit_root_does_not_read_referenced_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            report, stderr, code = run_checker(root, strict=False, include_audit_root=False)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)
            self.assertIn("audit_root_required", {failure["code"] for failure in report["failures"]})

    def test_non_strict_absolute_sidecar_is_not_read_without_audit_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            external = root.parent / f"external-scan-{root.name}.json"
            external.write_text("not-json", encoding="utf-8")
            try:
                manifest_path = root / "manifest.json"
                manifest = json.loads(manifest_path.read_text())
                manifest["visuals"][0]["source_scan_record_paths"] = [str(external)]
                manifest_path.write_text(json.dumps(manifest))
                report, stderr, code = run_checker(root, strict=False, include_audit_root=False)
                self.assertEqual(report["status"], "fail")
                self.assertNotIn("Traceback", stderr)
                self.assertEqual(code, 0)
                self.assertIn("audit_root_required", {failure["code"] for failure in report["failures"]})
                self.assertNotIn("invalid_input", {failure["code"] for failure in report["failures"]})
            finally:
                external.unlink(missing_ok=True)

    def test_tsv_manifest_boolean_is_parsed_and_extra_fields_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest = json.loads((root / "manifest.json").read_text())["visuals"][0]
            row = dict(manifest)
            for key in (
                "claim_ids",
                "source_ids",
                "source_cutout_asset_ids",
                "source_cutout_manifest_paths",
                "source_scan_record_paths",
            ):
                row[key] = "|".join(row[key])
            row["claim_bearing"] = "true"
            with (root / "manifest.tsv").open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(row), delimiter="\t")
                writer.writeheader()
                writer.writerow(row)
            report, stderr, code = run_checker(root, manifest_name="manifest.tsv")
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)
            with (root / "manifest.tsv").open("a", encoding="utf-8") as stream:
                stream.write("\t".join(["extra"] * (len(row) + 1)) + "\n")
            report, stderr, code = run_checker(root, manifest_name="manifest.tsv")
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("invalid_tsv_shape", {failure["code"] for failure in report["failures"]})

    def test_nested_review_state_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.pop("review")
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            codes = {failure["code"] for failure in report["failures"]}
            self.assertIn("review_missing", codes)

    def test_missing_claim_bearing_is_not_a_silent_nonclaim_skip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0].pop("claim_bearing")
            manifest["visuals"][0]["claim_ids"] = []
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("claim_bearing_missing", {failure["code"] for failure in report["failures"]})
            self.assertEqual(report["metrics"]["non_claim_bearing_visuals_skipped"], 0)

    def test_arbitrary_scan_json_is_not_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            (root / "records" / "scan.json").write_text(json.dumps({"arbitrary": True}))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_shared_scan_collection_with_target_and_other_visual_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            scan = json.loads((root / "records" / "scan.json").read_text())
            other = dict(scan)
            other["visual_id"] = "V-2"
            (root / "records" / "scan.json").write_text(json.dumps([scan, other]))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("audit_record_visual_join", {failure["code"] for failure in report["failures"]})

    def test_route_manifest_contract_field_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["source_scan_record_paths"] = []
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("route_field_join", {failure["code"] for failure in report["failures"]})

    def test_optional_generation_id_is_joined_across_scan_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["generation_id"] = "g-1"
            manifest_path.write_text(json.dumps(manifest))
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["generation_id"] = "g-1"
            contract_path.write_text(json.dumps(contract))
            scan_path = root / "records" / "scan.json"
            scan = json.loads(scan_path.read_text())
            scan["generation_id"] = "g-1"
            scan_path.write_text(json.dumps(scan))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)
            scan["generation_id"] = "g-2"
            scan_path.write_text(json.dumps(scan))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("audit_record_generation_join", {failure["code"] for failure in report["failures"]})

    def test_source_figure_route_does_not_ignore_scan_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="source_figure", route="source_figure")
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["kind"] = "source_figure"
            manifest["visuals"][0]["source_ids"] = ["S-1"]
            manifest_path.write_text(json.dumps(manifest))
            ledger_path = root / "ledger.json"
            ledger = json.loads(ledger_path.read_text())
            ledger["sources"] = [{"source_id": "S-1"}]
            ledger_path.write_text(json.dumps(ledger))
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.update({"kind": "source_figure", "source_ids": ["S-1"], "locator": "source page"})
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("source_figure_scan_forbidden", {failure["code"] for failure in report["failures"]})

    def test_source_figure_route_requires_source_figure_kind(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="table", route="source_figure")
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("source_route_kind_mismatch", {failure["code"] for failure in report["failures"]})

    def test_source_backed_faithful_reconstruction_cannot_be_not_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="source_figure", route="faithful_reconstruction")
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0].update({
                "kind": "source_figure",
                "source_ids": ["S-1"],
                "figure_id": "F-1",
                "rights_basis": "article32_quotation",
                "source_cutout_asset_ids": ["A-1"],
                "source_cutout_manifest_paths": ["records/cutout.json"],
                "source_scan_record_paths": [],
                "source_cutout_created_at": "2026-08-10T09:00:00+09:00",
                "derived_asset_id": "D-1",
                "derived_asset_path": "derived.txt",
                "visual_comparison_packet_path": "records/packet.json",
                "attribution_note": "Reconstructed by the survey",
                "decision_reason_code": "layout_unreadable",
                "reconstruction_created_at": "2026-08-10T09:01:00+09:00",
                "fidelity_status": "not_required",
                "visual_review_status": "passed",
            })
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            ledger_path = root / "ledger.json"
            ledger = json.loads(ledger_path.read_text())
            ledger["sources"] = [{"source_id": "S-1"}]
            ledger["assets"] = [{"asset_id": "A-1"}]
            ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.update({
                "kind": "source_figure",
                "source_ids": ["S-1"],
                "figure_id": "F-1",
                "rights_basis": "article32_quotation",
                "locator": "source page 2",
                "source_cutout_asset_ids": ["A-1"],
                "source_cutout_manifest_paths": ["records/cutout.json"],
                "source_scan_record_paths": [],
                "derived_asset_id": "D-1",
                "derived_asset_path": "derived.txt",
                "visual_comparison_packet_path": "records/packet.json",
                "attribution_note": "Reconstructed by the survey",
                "decision_reason_code": "layout_unreadable",
                "source_cutout_created_at": "2026-08-10T09:00:00+09:00",
                "reconstruction_created_at": "2026-08-10T09:01:00+09:00",
                "fidelity_status": "not_required",
                "visual_review_status": "passed",
            })
            contract["review"]["fidelity_status"] = "not_required"
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("reconstruction_fidelity_pending", {failure["code"] for failure in report["failures"]})

    def test_source_figure_sidecar_metadata_and_fidelity_join_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="source_figure", route="source_figure")
            (root / "source.bin").write_bytes(b"source material")
            (root / "output.bin").write_bytes(b"cutout")
            source_hash = hashlib.sha256((root / "source.bin").read_bytes()).hexdigest()
            output_hash = hashlib.sha256((root / "output.bin").read_bytes()).hexdigest()
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0].update({
                "kind": "source_figure",
                "source_ids": ["S-1"],
                "figure_id": "F-1",
                "rights_basis": "article32_quotation",
                "source_cutout_asset_ids": ["A-1"],
                "source_cutout_manifest_paths": ["records/cutout.json"],
                "source_scan_record_paths": [],
                "source_cutout_created_at": "2026-08-10T09:00:00+09:00",
                "fidelity_status": "passed",
                "visual_review_status": "not_required",
            })
            manifest_path.write_text(json.dumps(manifest))
            plot_path = root / "plot.json"
            plot = json.loads(plot_path.read_text())
            plot["rows"][0]["source_ids"] = ["S-1"]
            plot_path.write_text(json.dumps(plot))
            ledger_path = root / "ledger.json"
            ledger = json.loads(ledger_path.read_text())
            ledger["sources"] = [{"source_id": "S-1"}]
            ledger["assets"] = [{"asset_id": "A-1"}]
            ledger_path.write_text(json.dumps(ledger))
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.update({
                "kind": "source_figure",
                "source_ids": ["S-1"],
                "figure_id": "F-1",
                "rights_basis": "article32_quotation",
                "locator": "source page 2",
                "source_cutout_asset_ids": ["A-1"],
                "source_cutout_manifest_paths": ["records/cutout.json"],
                "source_scan_record_paths": [],
                "source_cutout_created_at": "2026-08-10T09:00:00+09:00",
                "fidelity_status": "passed",
                "visual_review_status": "not_required",
            })
            contract["review"]["fidelity_status"] = "passed"
            contract_path.write_text(json.dumps(contract))
            (root / "records" / "cutout.json").write_text(json.dumps({
                "asset_id": "A-1",
                "visual_id": "V-1",
                "asset_role": "source_cutout",
                "review_only": True,
                "figure_id": "F-1",
                "rights_basis": "article32_quotation",
                "fidelity_status": "passed",
                "claim_ids": ["C-1"],
                "source_id": "S-1",
                "source_sha256": source_hash,
                "output_sha256": output_hash,
                "source_hash_basis": "local_source_file",
                "local_source_path": "../source.bin",
                "output": "../output.bin",
            }))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)

            cutout_path = root / "records" / "cutout.json"
            cutout = json.loads(cutout_path.read_text())
            cutout.pop("visual_id")
            cutout_path.write_text(json.dumps(cutout))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("source_cutout_visual_join", {failure["code"] for failure in report["failures"]})

    def test_path_escape_and_missing_contract_are_failures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["contract_path"] = "../outside.json"
            manifest_path.write_text(json.dumps(manifest))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            manifest["visuals"][0].pop("contract_path")
            manifest_path.write_text(json.dumps(manifest))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)

    def test_nan_and_boolean_domain_values_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="chart")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["domain"]["min"] = True
            contract_path.write_text(json.dumps(contract))
            report, _, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotEqual(code, 0)

    def test_chart_domain_bounds_reject_arrays_and_objects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="chart")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["domain"]["min"] = [0]
            contract["semantics"]["domain"]["max"] = {"value": 10}
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("invalid_numeric_domain", {failure["code"] for failure in report["failures"]})

    def test_table_cartesian_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["cells"] = [[1, 2]]
            contract_path.write_text(json.dumps(contract))
            report, _, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotEqual(code, 0)

    def test_table_axis_mirror_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["axis_mirror"] = "rows = wrong; columns = wrong; cell = wrong; orientation = wrong"
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_diagram_endpoint_and_relation_are_declared(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="diagram")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"] = {
                "nodes": [{"id": "a", "meaning": "input"}, {"id": "b", "meaning": "output"}],
                "edges": [{"from": "a", "to": "missing", "relation": "causalish"}],
                "reading_order": ["a", "b"],
            }
            contract_path.write_text(json.dumps(contract))
            report, _, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotEqual(code, 0)

    def test_chart_comparator_and_domain_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="chart")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"].pop("comparator")
            contract["semantics"].pop("domain")
            contract_path.write_text(json.dumps(contract))
            report, _, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotEqual(code, 0)

    def test_category_chart_domain_requires_string_labels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="chart")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract["semantics"]["domain"] = {"type": "category", "labels": ["control", "task"]}
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)
            contract["semantics"]["domain"] = {"type": "category"}
            contract_path.write_text(json.dumps(contract))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_manifest_contract_route_and_status_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["source_visual_route"] = "inaccessible_source"
            manifest["visuals"][0]["semantic_status"] = "blocked"
            manifest_path.write_text(json.dumps(manifest))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_non_object_ledger_record_is_structured_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            ledger_path = root / "ledger.json"
            ledger = json.loads(ledger_path.read_text())
            ledger["claims"].append(True)
            ledger_path.write_text(json.dumps(ledger))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_comma_separated_join_ids_are_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["claim_ids"] = "C-1"
            manifest_path.write_text(json.dumps(manifest))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)

    def test_faithful_no_source_exception_has_scan_derived_packet_and_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, kind="source_figure", route="faithful_reconstruction")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.update({
                "kind": "source_figure",
                "locator": "source prose, results section",
                "derived_asset_id": "D-1",
                "derived_asset_path": "derived.txt",
                "visual_comparison_packet_path": "records/packet.json",
                "attribution_note": "Reconstructed by the survey",
                "visual_review_status": "passed",
                "fidelity_status": "passed",
                "reconstruction_created_at": "2026-08-10T09:01:00+09:00",
            })
            contract["review"]["fidelity_status"] = "passed"
            contract_path.write_text(json.dumps(contract))
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["kind"] = "source_figure"
            manifest["visuals"][0]["fidelity_status"] = "passed"
            manifest["visuals"][0]["visual_review_status"] = "passed"
            manifest_path.write_text(json.dumps(manifest))
            ledger_path = root / "ledger.json"
            ledger = json.loads(ledger_path.read_text())
            ledger["assets"] = [{"asset_id": "D-1"}]
            ledger_path.write_text(json.dumps(ledger))
            (root / "derived.txt").write_text("derived")
            (root / "records" / "packet.json").write_text(json.dumps({
                "visual_id": "V-1",
                "source_cutout_asset_ids": [],
                "derived_asset_id": "D-1",
                "claim_ids": ["C-1"],
                "decision_reason_code": "no_source_figure",
                "visual_review_status": "passed",
                "preserved_relation": "source relation retained",
                "changed_elements": "survey layout",
                "added_interpretation": "none",
            }))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("Traceback", stderr)
            self.assertEqual(code, 0)

            packet_path = root / "records" / "packet.json"
            packet = json.loads(packet_path.read_text())
            packet.pop("visual_id")
            packet_path.write_text(json.dumps(packet))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)
            self.assertIn("comparison_visual_join", {failure["code"] for failure in report["failures"]})

    def test_inaccessible_record_requires_access_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, route="inaccessible_source")
            (root / "records" / "scan.json").write_text(json.dumps({
                "record_type": "source_figure_access",
                "visual_id": "V-1",
                "source_visual_route": "inaccessible_source",
                "status": "inaccessible",
                "locator": "publisher page",
                "observed_at": "2026-08-10T09:00:00+09:00",
            }))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)

    def test_new_visual_no_source_is_not_the_faithful_exception(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_fixture(root, route="new_explanatory_visual")
            contract_path = root / "contracts" / "V-1.json"
            contract = json.loads(contract_path.read_text())
            contract.update({
                "derived_asset_id": "D-1",
                "derived_asset_path": "derived.txt",
                "visual_comparison_packet_path": "records/packet.json",
                "attribution_note": "Survey synthesis",
                "visual_review_status": "passed",
                "fidelity_status": "passed",
                "reconstruction_created_at": "2026-08-10T09:01:00+09:00",
            })
            contract["review"]["fidelity_status"] = "passed"
            contract_path.write_text(json.dumps(contract))
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["visuals"][0]["fidelity_status"] = "passed"
            manifest["visuals"][0]["visual_review_status"] = "passed"
            manifest_path.write_text(json.dumps(manifest))
            (root / "derived.txt").write_text("derived")
            (root / "records" / "packet.json").write_text(json.dumps({
                "source_cutout_asset_ids": [],
                "derived_asset_id": "D-1",
                "claim_ids": ["C-1"],
                "decision_reason_code": "no_source_figure",
                "visual_review_status": "passed",
                "preserved_relation": "source relation retained",
                "changed_elements": "survey layout",
                "added_interpretation": "none",
            }))
            report, stderr, code = run_checker(root)
            self.assertEqual(report["status"], "fail")
            self.assertNotIn("Traceback", stderr)
            self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
