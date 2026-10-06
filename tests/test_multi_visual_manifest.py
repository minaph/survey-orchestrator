#!/usr/bin/env python3
"""Complete two-figure fixtures and regression checks for nested page manifests."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import check_deck_quality as deck  # noqa: E402
from check_review_record import check_review_payload  # noqa: E402
from check_storyline_plot import check_plot_payload  # noqa: E402
from manifest_visuals import expand_manifest_visuals  # noqa: E402


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def two_figure_fixture(root: Path) -> tuple[dict, dict, dict]:
    """Synthetic source records test joins, without asserting scientific facts."""
    (root / "contracts").mkdir()
    (root / "records").mkdir()
    page = {
        "slide_id": "slide-1", "plot_version": "v0.1", "plot_row_id": "P-01",
        "section_id": "SEC-01", "evidence_block_id": "EB-01",
        "narrative_job": "compare the two source mechanisms", "evidence_class": "method",
        "citation_visible": "yes", "numeric": "no", "denominator_unit": "",
        "aggregation_level": "", "caveat_visible": "yes", "min_body_pt": "18",
        "protected_terms": "", "internal_vocab_free": "yes", "visuals": [],
    }
    ledger = {"claims": [], "sources": [], "assets": []}
    for number in (1, 2):
        vid, cid, sid, fid, aid = (f"{prefix}-{number}" for prefix in ("V", "C", "S", "F", "A"))
        source = root / f"source-{number}.bin"
        output = root / f"cutout-{number}.bin"
        source.write_bytes(f"synthetic source {number}".encode())
        output.write_bytes(f"synthetic cutout {number}".encode())
        visual = {
            "visual_id": vid, "kind": "source_figure", "claim_bearing": True,
            "claim_ids": [cid], "source_ids": [sid], "figure_id": fid,
            "contract_path": f"contracts/{vid}.json", "primary_visual_type": "source_figure",
            "source_pointer": f"Synthetic source {number}, figure 1",
            "source_visual_route": "source_figure", "reader_role": "mechanism explanation",
            "boundary": "synthetic fixture only", "status": "SOURCE-REPORTED",
            "semantic_status": "passed", "fidelity_status": "passed",
            "visual_review_status": "not_required", "rights_basis": "article32_quotation",
            "source_cutout_asset_ids": [aid],
            "source_cutout_manifest_paths": [f"records/{aid}.json"],
            "source_scan_record_paths": [], "decision_reason_code": "",
            "source_cutout_created_at": "2026-08-10T09:00:00+09:00",
        }
        page["visuals"].append(visual)
        contract = dict(visual)
        contract.update({
            "slide_id": "slide-1", "locator": "synthetic source, figure 1",
            "semantics": {"observation": "synthetic mechanism fixture"},
            "review": {"deterministic_status": "passed", "semantic_status": "passed", "fidelity_status": "passed"},
        })
        write_json(root / "contracts" / f"{vid}.json", contract)
        write_json(root / "records" / f"{aid}.json", {
            "asset_id": aid, "visual_id": vid, "asset_role": "source_cutout", "review_only": True,
            "figure_id": fid, "rights_basis": "article32_quotation", "fidelity_status": "passed",
            "claim_ids": [cid], "source_id": sid, "source_hash_basis": "local_source_file",
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "local_source_path": f"../{source.name}", "output": f"../{output.name}",
        })
        ledger["claims"].append({"claim_id": cid})
        ledger["sources"].append({"source_id": sid})
        ledger["assets"].append({"asset_id": aid})
    plot = {
        "plot_version": "v0.1", "plot_scope": "target_survey", "plot_status": "verified",
        "rows": [{
            "plot_row_id": "P-01", "section_id": "SEC-01", "evidence_block_id": "EB-01",
            "slide_id": "slide-1", "visual_ids": ["V-1", "V-2"],
            "claim_ids": ["C-1", "C-2"], "source_ids": ["S-1", "S-2"],
            "T": "How do the mechanisms differ?", "B": "Two source mechanisms are introduced.",
            "Bottom": "The comparison is restricted to these synthetic fixtures.",
            "Figure": "Each source figure shows its own mechanism.", "Next": "Which conditions limit the comparison?",
        }],
    }
    review = {
        "plot_review": {
            "status": "passed", "plot_version": "v0.1",
            "scope": {"coverage": "all", "rows": ["P-01"], "pages": ["slide-1"]},
            "findings": [],
        },
        "reader_review": {
            "status": "passed",
            "scope": {"coverage": "all", "pages": ["slide-1"], "items": ["V-1", "V-2"]},
            "findings": [{
                "claim_or_visual": f"V-{number}", "page": "slide-1",
                "question": "Does this figure support its own attributed summary?",
                "verdict": "adequate", "repair": "none", "recheck": "Inspect this source and figure independently.",
            } for number in (1, 2)],
        },
        "deterministic": {"status": "passed"}, "semantic": {"status": "passed"},
        "fidelity": {"status": "passed"}, "visual_review": {"status": "passed"}, "release": "passed",
    }
    write_json(root / "manifest.json", {"slides": [page]})
    write_json(root / "ledger.json", ledger)
    write_json(root / "plot.json", plot)
    write_json(root / "review.json", review)
    write_tsv(root / "manifest.tsv", page)
    # This minimal OPC fixture contains one slide and two picture objects.
    # It exercises observed page/object counts, not rendered visual quality.
    with zipfile.ZipFile(root / "deck.pptx", "w") as archive:
        archive.writestr("[Content_Types].xml", '''<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>''')
        archive.writestr("_rels/.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>')
        archive.writestr("ppt/_rels/presentation.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>')
        archive.writestr("ppt/presentation.xml", '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/></p:presentation>')
        archive.writestr("ppt/slides/slide1.xml", '''<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>
<p:sp><p:nvSpPr><p:cNvPr id="2" name="Heading"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="100000" y="100000"/><a:ext cx="8000000" cy="1000000"/></a:xfrm></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr sz="2000"/><a:t>J. Alpha+ and J. Beta+: two source mechanisms</a:t></a:r></a:p></p:txBody></p:sp>
<p:pic><p:nvPicPr><p:cNvPr id="3" name="Figure 1"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1"/></p:blipFill><p:spPr><a:xfrm><a:off x="100000" y="1500000"/><a:ext cx="1000000" cy="1000000"/></a:xfrm></p:spPr></p:pic>
<p:pic><p:nvPicPr><p:cNvPr id="4" name="Figure 2"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1"/></p:blipFill><p:spPr><a:xfrm><a:off x="2000000" y="1500000"/><a:ext cx="1000000" cy="1000000"/></a:xfrm></p:spPr></p:pic>
</p:spTree></p:cSld></p:sld>''')
        archive.writestr("ppt/slides/_rels/slide1.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/></Relationships>')
        archive.writestr("ppt/media/image1.png", base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
        ))
    return page, plot, review


def write_tsv(path: Path, page: dict) -> None:
    row = dict(page)
    row["visuals"] = json.dumps(row["visuals"])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row), delimiter="\t")
        writer.writeheader()
        writer.writerow(row)


def run_preflight(root: Path, manifest: str = "manifest.json") -> tuple[dict, int]:
    result = subprocess.run([
        sys.executable, str(SKILL_ROOT / "scripts" / "check_evidence_visual_contract.py"),
        "--manifest", str(root / manifest), "--ledger", str(root / "ledger.json"),
        "--plot", str(root / "plot.json"), "--audit-root", str(root), "--strict",
    ], capture_output=True, text=True)
    if result.stderr:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout), result.returncode


class MultiVisualManifestTests(unittest.TestCase):
    def test_optional_cover_visual_before_or_after_evidence_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page, _plot, _review = two_figure_fixture(root)
            cover = {
                "slide_id": "slide-2", "evidence_class": "cover",
                "visuals": [{
                    "visual_id": "V-COVER", "kind": "diagram", "claim_bearing": False,
                    "primary_visual_type": "none", "source_visual_route": "not_applicable",
                }],
            }
            for rows in ([cover, page], [page, cover]):
                with self.subTest(cover_first=rows[0] is cover):
                    errors, warnings = deck.check_visual_contract_links(rows, root, True)
                    self.assertEqual(errors, [])
                    self.assertEqual(warnings, [])

    def test_cover_order_cannot_hide_missing_claim_visual_contract_fields(self) -> None:
        for missing_field in ("contract_path", "semantic_status", "reader_role", "boundary", "status"):
            with self.subTest(missing_field=missing_field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                page, _plot, _review = two_figure_fixture(root)
                page["visuals"][1].pop(missing_field)
                cover = {
                    "slide_id": "slide-2", "evidence_class": "cover",
                    "visuals": [{
                        "visual_id": "V-COVER", "kind": "diagram", "claim_bearing": False,
                        "primary_visual_type": "none", "source_visual_route": "not_applicable",
                    }],
                }
                for rows in ([cover, page], [page, cover]):
                    errors, _warnings = deck.check_visual_contract_links(rows, root, True)
                    self.assertTrue(any(
                        "visual V-2" in error and "requires contract columns" in error and missing_field in error
                        for error in errors
                    ))

    def test_complete_json_and_tsv_preflight_check_both_figures(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            two_figure_fixture(root)
            for manifest in ("manifest.json", "manifest.tsv"):
                with self.subTest(manifest=manifest):
                    report, code = run_preflight(root, manifest)
                    self.assertEqual(report["failures"], [])
                    self.assertEqual(code, 0)
                    self.assertEqual(report["metrics"]["manifest_pages"], 1)
                    self.assertEqual(report["metrics"]["manifest_visuals"], 2)
                    self.assertEqual(report["metrics"]["claim_bearing_visuals"], 2)
                    self.assertEqual(report["metrics"]["contracts_loaded"], 2)

    def test_complete_observer_keeps_one_page_and_checks_two_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            two_figure_fixture(root)
            result = subprocess.run([
                sys.executable, str(SKILL_ROOT / "scripts" / "check_deck_quality.py"),
                "--manifest", str(root / "manifest.tsv"), "--pptx", str(root / "deck.pptx"),
                "--plot", str(root / "plot.json"), "--review-record", str(root / "review.json"),
                "--audit-root", str(root), "--strict",
            ], capture_output=True, text=True)
            self.assertEqual(result.stderr, "")
            report = json.loads(result.stdout)
            self.assertEqual(report["failures"], [])
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["metrics"]["manifest_rows"], 1)
            self.assertEqual(report["metrics"]["manifest_visuals"], 2)
            self.assertEqual(report["metrics"]["pptx"]["slide_count"], 1)
            self.assertEqual(report["metrics"]["observed"]["PPTX"]["evidence_rows"], 1)
            self.assertEqual(report["metrics"]["observed"]["PPTX"]["observed_evidence_visual_object_rows"], 1)

    def test_second_visual_contract_route_and_review_defects_fail(self) -> None:
        for field, value in (("visual_id", "V-WRONG"), ("source_visual_route", "inaccessible_source"), ("semantic_status", "pending")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                page, _plot, _review = two_figure_fixture(root)
                contract_path = root / "contracts" / "V-2.json"
                contract = json.loads(contract_path.read_text())
                contract[field] = value
                write_json(contract_path, contract)
                report, code = run_preflight(root)
                self.assertNotEqual(code, 0)
                self.assertTrue(any(failure.get("visual_id") == "V-2" for failure in report["failures"]))
                errors, _warnings = deck.check_visual_contract_links([page], root, True)
                self.assertTrue(errors)

    def test_second_visual_sidecar_join_fails_in_both_checkers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            two_figure_fixture(root)
            path = root / "records" / "A-2.json"
            sidecar = json.loads(path.read_text())
            sidecar["source_id"] = "S-1"
            write_json(path, sidecar)
            report, code = run_preflight(root)
            self.assertNotEqual(code, 0)
            self.assertTrue(any(failure.get("visual_id") == "V-2" for failure in report["failures"]))
            _rows, errors, _warnings = deck.read_manifest(root / "manifest.tsv", True, root, True)
            self.assertTrue(any("source_id" in error for error in errors))

    def test_second_visual_cannot_borrow_first_visual_joins(self) -> None:
        for key in ("source_ids", "claim_ids", "source_cutout_asset_ids", "contract_path"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                page, _plot, _review = two_figure_fixture(root)
                page["visuals"][1].pop(key)
                write_json(root / "manifest.json", {"slides": [page]})
                report, code = run_preflight(root)
                self.assertNotEqual(code, 0)
                self.assertTrue(any(failure.get("visual_id") == "V-2" for failure in report["failures"]))

    def test_second_visual_plot_joins_cannot_be_omitted(self) -> None:
        for key in ("visual_ids", "claim_ids", "source_ids"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                page, plot, _review = two_figure_fixture(root)
                plot["rows"][0][key].pop()
                errors, _warnings, metrics = check_plot_payload(plot, [page], strict=True)
                self.assertTrue(errors)
                self.assertEqual(metrics["manifest_rows"], 1)
                write_json(root / "plot.json", plot)
                _report, code = run_preflight(root)
                self.assertNotEqual(code, 0)

    def test_second_visual_reader_review_scope_cannot_be_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page, plot, review = two_figure_fixture(Path(directory))
            review["reader_review"]["scope"]["items"] = ["V-1"]
            review["reader_review"]["findings"] = review["reader_review"]["findings"][:1]
            errors, _warnings, metrics = check_review_payload(review, plot["rows"], [page], strict=True)
            self.assertTrue(any("omits nested visuals" in error for error in errors))
            self.assertEqual(metrics["manifest_pages"], 1)

    def test_invalid_nested_input_and_page_overrides_are_rejected(self) -> None:
        page = {"slide_id": "slide-1", "plot_row_id": "P-01", "visuals": [{"visual_id": "V-1"}, {"visual_id": "V-2"}]}
        changes = [
            {"visuals": "["}, {"visuals": []}, {"visuals": {}}, {"visuals": [None]},
            {"visual_id": "V-OLD"}, {"source_ids": ["S-OLD"]},
            {"visuals": [{"visual_id": "V-1", "slide_id": "slide-2"}]},
            {"visuals": [{"visual_id": "V-1", "evidence_class": "cover"}]},
            {"visuals": [{"visual_id": "V-1", "plotRowId": "P-02"}]},
            {"visuals": [{"visual_id": "V-1", "visuals": []}]},
            {"visuals": [{"visual_id": "V-1"}, {"visual_id": "V-1"}]},
            {"visuals": [{"visual_id": True}]},
            {"visuals": [{"visual_id": "V-1", "contract_path": 42}]},
        ]
        for change in changes:
            with self.subTest(change=change):
                _visuals, errors = expand_manifest_visuals([{**page, **change}])
                self.assertTrue(errors)

    def test_legacy_and_equal_child_page_fields_are_preserved(self) -> None:
        legacy = {"slide_id": "slide-1", "visual_id": "V-1", "claim_ids": ["C-1"]}
        visuals, errors = expand_manifest_visuals([legacy])
        self.assertEqual(errors, [])
        self.assertEqual(visuals, [legacy])
        page = {"slide_id": "slide-1", "plot_row_id": "P-01", "visuals": [{"visual_id": "V-1", "slideId": "slide-1"}]}
        visuals, errors = expand_manifest_visuals([page])
        self.assertEqual(errors, [])
        self.assertEqual(visuals[0]["plot_row_id"], "P-01")
        self.assertNotIn("slideId", visuals[0])

    def test_observed_page_metrics_do_not_double_count_numeric_or_font_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page, _plot, _review = two_figure_fixture(Path(directory))
            page["numeric"] = "yes"
            metrics, errors, _warnings = deck.validate_observed_artifact([page], {1: {
                "numeric_tokens": ["20 ms"], "citation": True, "has_observed_visual": True,
                "font_sizes_pt": [20], "body_candidate_font_sizes_pt": [20], "text": "J. Alpha+ J. Beta+",
            }}, strict=True)
            self.assertEqual(errors, [])
            self.assertEqual(metrics["numeric_pages"], [1])
            self.assertEqual(metrics["evidence_rows"], 1)

    def test_second_reconstruction_requires_its_own_observed_attribution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page, _plot, _review = two_figure_fixture(Path(directory))
            for number, visual in enumerate(page["visuals"], start=1):
                visual["source_visual_route"] = "faithful_reconstruction"
                visual["attribution_note"] = f"Reconstructed by the survey: source mechanism {number}"
            observed = {"citation": True, "has_observed_visual": True, "text": page["visuals"][0]["attribution_note"]}
            _metrics, errors, _warnings = deck.validate_observed_artifact([page], {1: observed}, strict=True)
            self.assertEqual(len(errors), 1)
            self.assertIn("visual V-2", errors[0])
            observed["text"] += " " + page["visuals"][1]["attribution_note"]
            _metrics, errors, _warnings = deck.validate_observed_artifact([page], {1: observed}, strict=True)
            self.assertEqual(errors, [])

    def test_duplicate_page_rows_remain_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page, _plot, _review = two_figure_fixture(root)
            with (root / "manifest.tsv").open("a", encoding="utf-8", newline="") as stream:
                row = dict(page)
                row["visuals"] = json.dumps(row["visuals"])
                csv.DictWriter(stream, fieldnames=list(row), delimiter="\t").writerow(row)
            _rows, errors, _warnings = deck.read_manifest(root / "manifest.tsv", True, root, True)
            self.assertTrue(any("duplicate slide/page" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
