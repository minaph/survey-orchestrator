#!/usr/bin/env python3
"""Check the formal shape and coverage of a qualitative review record.

This checker does not decide whether a plot is clear, a visual is meaningful,
or a semantic verdict is correct. It only prevents a strict release from
silently omitting the plot/reader review, its declared scope, or its repair
and recheck fields.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any
from manifest_visuals import expand_manifest_visuals, has_nested_visuals


REVIEW_STATUSES = {"passed", "pending", "blocked"}
FINDING_VERDICTS = {"strong", "adequate", "fragile", "blocked"}
COMPONENT_STATUSES = {"passed", "pending", "blocked", "not_required", "not_applicable"}
STRICT_COMPONENT_PASS = {
    "deterministic": {"passed"},
    "semantic": {"passed"},
    "fidelity": {"passed", "not_required", "not_applicable"},
    "visual_review": {"passed", "not_required", "not_applicable"},
}


def _values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    delimiter = "|" if "|" in text else ","
    return [item.strip() for item in text.split(delimiter) if item.strip()]


def _ids(rows: list[dict[str, Any]], *names: str) -> set[str]:
    result: set[str] = set()
    for row in rows:
        for name in names:
            value = row.get(name)
            if value is not None:
                result.update(_values(value))
                break
    return result


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _check_scope(
    review: dict[str, Any],
    label: str,
    *,
    expected_rows: set[str],
    expected_pages: set[str],
    expected_items: set[str],
    strict: bool,
    errors: list[str],
) -> dict[str, Any]:
    scope = review.get("scope")
    if not isinstance(scope, dict):
        errors.append(f"{label}.scope must be an object")
        return {"rows": 0, "pages": 0, "coverage": ""}
    rows = set(_values(scope.get("rows", scope.get("plot_row_ids"))))
    pages = set(_values(scope.get("pages", scope.get("slide_ids"))))
    items = set(_values(scope.get("items", scope.get("claim_or_visuals"))))
    coverage = str(scope.get("coverage", "")).strip().lower()
    if not coverage:
        errors.append(f"{label}.scope.coverage is required")
    elif coverage not in {"all", "sample"}:
        errors.append(f"{label}.scope.coverage must be all or sample")
    if not rows and label == "plot_review":
        errors.append("plot_review.scope.rows is required")
    if not pages:
        errors.append(f"{label}.scope.pages is required")
    if strict and coverage == "all":
        if label == "plot_review":
            missing_rows = sorted(expected_rows - rows)
            if missing_rows:
                errors.append(f"{label}.scope omits plot rows: {missing_rows[:12]}")
        missing_pages = sorted(expected_pages - pages)
        if missing_pages:
            errors.append(f"{label}.scope omits slide pages: {missing_pages[:12]}")
    if label == "plot_review":
        unknown_rows = sorted(rows - expected_rows)
        if unknown_rows:
            errors.append(f"{label}.scope has unknown plot rows: {unknown_rows[:12]}")
    unknown_pages = sorted(pages - expected_pages)
    if unknown_pages:
        errors.append(f"{label}.scope has unknown slide pages: {unknown_pages[:12]}")
    unknown_items = sorted(items - expected_items)
    if unknown_items:
        errors.append(f"{label}.scope has unknown claim/visual locators: {unknown_items[:12]}")
    if coverage == "sample" and strict and label == "plot_review":
        central_rows = set(_values(scope.get("central_rows")))
        if not central_rows:
            errors.append("plot_review.scope.central_rows is required for a sampled plot review")
        elif not central_rows <= rows:
            errors.append("plot_review.scope.central_rows must be included in scope.rows")
    return {"rows": len(rows), "pages": len(pages), "items": len(items), "coverage": coverage}


def _check_findings(
    review: dict[str, Any],
    label: str,
    errors: list[str],
    *,
    scope_rows: set[str],
    scope_pages: set[str],
    scope_items: set[str],
    expected_items: set[str],
) -> int:
    findings = review.get("findings", [])
    if not isinstance(findings, list):
        errors.append(f"{label}.findings must be an array")
        return 0
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"{label}.findings[{index}] must be an object")
            continue
        required_keys = ("page", "question", "verdict", "repair", "recheck")
        for key in required_keys:
            if key not in finding:
                errors.append(f"{label}.findings[{index}] lacks {key}")
        row_value = str(finding.get("row", "")).strip()
        item_value = str(finding.get("claim_or_visual", "")).strip()
        if bool(row_value) == bool(item_value):
            errors.append(
                f"{label}.findings[{index}] must provide exactly one of row or claim_or_visual"
            )
        row = row_value or item_value
        page = str(finding.get("page", "")).strip()
        question = str(finding.get("question", "")).strip()
        verdict = str(finding.get("verdict", "")).strip().lower()
        repair = str(finding.get("repair", "")).strip()
        recheck = str(finding.get("recheck", "")).strip()
        if not row:
            errors.append(f"{label}.findings[{index}] needs a non-empty row/claim_or_visual locator")
        elif item_value and not row_value:
            if not scope_items:
                errors.append(f"{label}.findings[{index}] claim_or_visual requires scope.items")
            elif item_value not in scope_items:
                errors.append(f"{label}.findings[{index}] claim/visual locator is outside declared scope: {item_value}")
            if item_value not in expected_items:
                errors.append(f"{label}.findings[{index}] has unknown claim/visual locator: {item_value}")
        elif scope_rows and row not in scope_rows:
            errors.append(f"{label}.findings[{index}] row is outside declared scope: {row}")
        if not page:
            errors.append(f"{label}.findings[{index}] needs a non-empty page locator")
        elif scope_pages and page not in scope_pages:
            errors.append(f"{label}.findings[{index}] page is outside declared scope: {page}")
        if not question:
            errors.append(f"{label}.findings[{index}] question must be non-empty")
        if not verdict or verdict not in FINDING_VERDICTS:
            errors.append(f"{label}.findings[{index}] has invalid verdict={verdict!r}")
        if not repair:
            errors.append(f"{label}.findings[{index}] repair must be explicit; use none when no repair is needed")
        if not recheck:
            errors.append(f"{label}.findings[{index}] recheck must be non-empty")
    return len(findings)


def check_review_payload(
    payload: Any,
    plot_rows: list[dict[str, Any]] | None = None,
    manifest_rows: list[dict[str, Any]] | None = None,
    *,
    strict: bool = False,
    expected_plot_version: str | None = None,
) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(payload, dict):
        return ["review record must be a JSON object"], warnings, {}
    plot_review = payload.get("plot_review")
    reader_review = payload.get("reader_review")
    if not isinstance(plot_review, dict):
        errors.append("review record lacks plot_review object")
        plot_review = {}
    if not isinstance(reader_review, dict):
        errors.append("review record lacks reader_review object")
        reader_review = {}
    release = str(payload.get("release", "")).strip().lower()
    if release not in {"passed", "pending", "blocked"}:
        errors.append("review record release must be passed, pending, or blocked")
    elif strict and release != "passed":
        errors.append("strict release requires review record release=passed")

    expected_rows = _ids(plot_rows or [], "plot_row_id", "row_id", "id")
    expected_pages = _ids(manifest_rows or [], "slide_id", "slideId")
    visual_rows, visual_errors = expand_manifest_visuals(manifest_rows or [])
    errors.extend(visual_errors)
    expected_items = _ids(visual_rows, "visual_id", "visualId", "claim_ids", "claimIds")
    nested_pages = _ids(
        [row for row in manifest_rows or [] if has_nested_visuals(row)], "slide_id", "slideId"
    )
    metrics: dict[str, Any] = {
        "plot_rows": len(expected_rows),
        "manifest_pages": len(expected_pages),
        "reviewable_claim_visuals": len(expected_items),
        "release": release,
        "plot_review_findings": 0,
        "reader_review_findings": 0,
    }
    for label, review in (("plot_review", plot_review), ("reader_review", reader_review)):
        status = str(review.get("status", "")).strip().lower()
        if status not in REVIEW_STATUSES:
            errors.append(f"{label}.status must be passed, pending, or blocked")
        elif strict and status != "passed":
            errors.append(f"strict release requires {label}.status=passed")
        if label == "plot_review":
            plot_version = str(review.get("plot_version", "")).strip()
            if not plot_version:
                errors.append("plot_review.plot_version is required")
            elif expected_plot_version is not None and plot_version != expected_plot_version:
                errors.append(
                    f"plot_review.plot_version={plot_version!r} does not match current plot_version={expected_plot_version!r}"
                )
        scope = review.get("scope") if isinstance(review.get("scope"), dict) else {}
        scope_rows = set(_values(scope.get("rows", scope.get("plot_row_ids"))))
        scope_pages = set(_values(scope.get("pages", scope.get("slide_ids"))))
        scope_items = set(_values(scope.get("items", scope.get("claim_or_visuals"))))
        if strict and label == "reader_review":
            review_pages = expected_pages if scope.get("coverage") == "all" else scope_pages
            required_visuals = _ids(
                [
                    row for row in visual_rows
                    if str(row.get("slide_id", row.get("slideId", ""))) in nested_pages & review_pages
                ],
                "visual_id", "visualId",
            )
            missing_visuals = sorted(required_visuals - scope_items)
            if missing_visuals:
                errors.append(f"reader_review.scope omits nested visuals: {missing_visuals[:12]}")
        metrics["plot_review_scope" if label == "plot_review" else "reader_review_scope"] = _check_scope(
            review,
            label,
            expected_rows=expected_rows,
            expected_pages=expected_pages,
            expected_items=expected_items,
            strict=strict,
            errors=errors,
        )
        finding_count = _check_findings(
            review,
            label,
            errors,
            scope_rows=scope_rows,
            scope_pages=scope_pages,
            scope_items=scope_items,
            expected_items=expected_items,
        )
        metrics["plot_review_findings" if label == "plot_review" else "reader_review_findings"] = finding_count

    component_values: dict[str, str] = {}
    for component in STRICT_COMPONENT_PASS:
        allowed = COMPONENT_STATUSES
        raw_component = payload.get(component)
        if not isinstance(raw_component, dict):
            errors.append(f"review record lacks {component} object")
            continue
        status = str(raw_component.get("status", "")).strip().lower()
        if status not in allowed:
            errors.append(f"{component}.status must be one of {sorted(allowed)}")
            continue
        component_values[component] = status
        if strict and status not in STRICT_COMPONENT_PASS[component]:
            errors.append(f"strict release requires {component}.status in {sorted(STRICT_COMPONENT_PASS[component])}")
    if release == "passed":
        unresolved = sorted(
            name for name, status in component_values.items()
            if status in {"pending", "blocked"}
        )
        if unresolved:
            errors.append(f"review record release=passed conflicts with unresolved components: {unresolved}")

    if "score" in reader_review:
        score = reader_review.get("score")
        if not _finite_number(score) or score < 0 or score > 100:
            errors.append("reader_review.score must be a finite number from 0 to 100")
        denominator = reader_review.get("denominator")
        if denominator is None or not _finite_number(denominator) or denominator <= 0:
            errors.append("reader_review.denominator must be a positive finite number")
    elif strict:
        warnings.append("reader_review.score is omitted; qualitative dimensions remain authoritative")

    metrics["status"] = "fail" if errors else "pass"
    return errors, warnings, metrics


def check_review_file(
    path: Path,
    plot_rows: list[dict[str, Any]] | None = None,
    manifest_rows: list[dict[str, Any]] | None = None,
    *,
    strict: bool = False,
    expected_plot_version: str | None = None,
) -> tuple[list[str], list[str], dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"review record could not be read: {exc}"], [], {"review_path": str(path)}
    errors, warnings, metrics = check_review_payload(
        payload,
        plot_rows,
        manifest_rows,
        strict=strict,
        expected_plot_version=expected_plot_version,
    )
    metrics["review_path"] = str(path)
    return errors, warnings, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", "--review-record", dest="review", type=Path, required=True)
    parser.add_argument("--plot", "--storyline-plot", dest="plot", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    plot_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    plot_version: str | None = None
    if args.plot:
        from check_storyline_plot import _load_payload, plot_rows as get_plot_rows

        plot_payload, load_errors = _load_payload(args.plot)
        if load_errors:
            report = {"status": "fail", "failures": load_errors, "warnings": [], "metrics": {}}
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 2 if args.strict else 0
        plot_rows = get_plot_rows(plot_payload)
        if isinstance(plot_payload, dict):
            plot_version = str(plot_payload.get("plot_version", "")).strip() or None
    if args.manifest:
        with args.manifest.open("r", encoding="utf-8-sig", newline="") as stream:
            import csv

            manifest_rows = list(csv.DictReader(stream, delimiter="\t"))
    errors, warnings, metrics = check_review_file(
        args.review,
        plot_rows,
        manifest_rows,
        strict=args.strict,
        expected_plot_version=plot_version,
    )
    report = {"status": "fail" if errors else "pass", "failures": errors, "warnings": warnings, "metrics": metrics}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
