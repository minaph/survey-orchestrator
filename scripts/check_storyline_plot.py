#!/usr/bin/env python3
"""Check deterministic joins between a storyline plot and a slide manifest.

This checker validates presence, identifiers, and coverage only. It does not
judge whether a plot is clear, whether a visual is meaningful, or whether a
claim is supported; those remain qualitative reviewer decisions.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any
from manifest_visuals import expand_manifest_visuals


PLOT_STATUSES = {
    "idea", "searching", "evidence_pending", "draft", "verified",
    "blocked", "deferred", "synthesis",
}
FINAL_PLOT_STATUSES = {"verified", "synthesis"}
PLOT_SCOPES = {"target_survey", "reference_artifact", "source_analysis", "working_note"}


def _field(record: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in record:
            return record[name]
    return default


def _values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    delimiter = "|" if "|" in text else ","
    return [item.strip() for item in text.split(delimiter) if item.strip()]


def _raw_plot_rows(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in ("rows", "slides", "items", "plot"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _load_payload(path: Path) -> tuple[Any, list[str]]:
    try:
        if path.suffix.casefold() in {".tsv", ".csv"}:
            delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream, delimiter=delimiter))
            first = rows[0] if rows else {}
            return {
                "plot_version": first.get("plot_version", ""),
                "plot_scope": first.get("plot_scope", ""),
                "plot_status": first.get("plot_status", ""),
                "rows": rows,
            }, []
        if path.suffix.casefold() == ".jsonl":
            rows: list[Any] = []
            with path.open("r", encoding="utf-8-sig") as stream:
                for line_number, line in enumerate(stream, start=1):
                    if not line.strip():
                        continue
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        return None, [f"storyline plot JSONL line {line_number} could not be read: {exc}"]
            first = rows[0] if rows and isinstance(rows[0], dict) else {}
            return {
                "plot_version": first.get("plot_version", ""),
                "plot_scope": first.get("plot_scope", ""),
                "plot_status": first.get("plot_status", ""),
                "rows": rows,
            }, []
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        return None, [f"storyline plot could not be read: {exc}"]


def plot_rows(payload: Any) -> list[dict[str, Any]]:
    return [row for row in _raw_plot_rows(payload) if isinstance(row, dict)]


def _plot_status(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("plot_status", payload.get("status", ""))).strip().lower()


def check_plot_payload(
    payload: Any,
    manifest_rows: list[dict[str, Any]] | None = None,
    *,
    strict: bool = False,
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Return deterministic errors, warnings, and coverage metrics."""
    errors: list[str] = []
    warnings: list[str] = []
    raw_rows = _raw_plot_rows(payload)
    rows = [row for row in raw_rows if isinstance(row, dict)]
    if not isinstance(payload, dict):
        errors.append("storyline plot must be a JSON object")
        return errors, warnings, {"plot_rows": 0}
    version = str(payload.get("plot_version", "")).strip()
    scope = str(payload.get("plot_scope", "")).strip().lower()
    status = _plot_status(payload)
    if not version:
        errors.append("storyline plot lacks plot_version")
    if scope not in PLOT_SCOPES:
        errors.append(f"storyline plot has invalid plot_scope={scope!r}")
    if strict and manifest_rows is not None and scope != "target_survey":
        errors.append("strict manifest joins require plot_scope=target_survey; keep reference plots separate")
    if status not in PLOT_STATUSES:
        errors.append(f"storyline plot has invalid plot_status={status!r}")
    if strict and status not in FINAL_PLOT_STATUSES:
        errors.append("strict release requires plot_status=verified or synthesis")
    if not rows:
        errors.append("storyline plot contains no rows/slides/items")
    if len(rows) != len(raw_rows):
        errors.append("storyline plot contains a non-object row/item")

    by_row: dict[str, dict[str, Any]] = {}
    block_sections: dict[str, str] = {}
    for index, row in enumerate(rows):
        row_id = str(_field(row, "plot_row_id", "row_id", "id", default="")).strip()
        block_id = str(_field(row, "evidence_block_id", "evidenceBlockId", default="")).strip()
        section_id = str(_field(row, "section_id", "sectionId", default="")).strip()
        if not row_id:
            errors.append(f"storyline plot row {index}: missing plot_row_id")
            continue
        if row_id in by_row:
            errors.append(f"storyline plot contains duplicate plot_row_id={row_id}")
        else:
            by_row[row_id] = row
        if not section_id:
            errors.append(f"plot row {row_id}: missing section_id")
        if not block_id:
            errors.append(f"plot row {row_id}: missing evidence_block_id")
        elif block_id in block_sections and block_sections[block_id] != section_id:
            errors.append(f"evidence_block_id={block_id} is assigned to multiple sections")
        else:
            block_sections[block_id] = section_id
        if strict:
            for label, aliases in (
                ("T", ("T", "title", "question")),
                ("B", ("B", "body")),
                ("Bottom", ("Bottom", "bottom", "takeaway")),
                ("Figure", ("Figure", "figure_relation", "figureRelation")),
                ("Next", ("Next", "next_question", "nextQuestion")),
            ):
                if not str(_field(row, *aliases, default="")).strip():
                    errors.append(f"plot row {row_id}: missing {label}")

    metrics: dict[str, Any] = {
        "plot_version": version,
        "plot_scope": scope,
        "plot_status": status,
        "plot_rows": len(rows),
        "manifest_rows": len(manifest_rows or []),
        "joined_manifest_rows": 0,
        "unjoined_plot_rows": 0,
    }
    if manifest_rows is None:
        return errors, warnings, metrics

    visual_rows, visual_errors = expand_manifest_visuals(manifest_rows)
    errors.extend(visual_errors)
    metrics["manifest_visuals"] = len(visual_rows)

    manifest_row_ids: set[str] = set()
    manifest_visual_ids: set[str] = set()
    manifest_slide_ids: set[str] = set()
    joined_pages: set[tuple[str, str]] = set()
    for index, manifest in enumerate(visual_rows):
        sid = str(_field(manifest, "slide_id", "slideId", default="")).strip()
        row_id = str(_field(manifest, "plot_row_id", "plotRowId", default="")).strip()
        manifest_row_ids.add(row_id)
        if sid:
            manifest_slide_ids.add(sid)
        visual_id = str(_field(manifest, "visual_id", "visualId", default="")).strip()
        if visual_id:
            manifest_visual_ids.add(visual_id)
        if not row_id:
            errors.append(f"manifest row {sid or index}: missing plot_row_id")
            continue
        plot_row = by_row.get(row_id)
        if plot_row is None:
            errors.append(f"manifest row {sid or index}: plot_row_id={row_id} does not join to plot")
            continue
        joined_pages.add((sid, row_id))
        metrics["joined_manifest_rows"] = len(joined_pages)
        manifest_version = str(_field(manifest, "plot_version", "plotVersion", default="")).strip()
        if manifest_version != version:
            errors.append(f"manifest row {sid or index}: plot_version does not match storyline plot")
        manifest_section = str(_field(manifest, "section_id", "sectionId", default="")).strip()
        plot_section = str(_field(plot_row, "section_id", "sectionId", default="")).strip()
        if manifest_section != plot_section:
            errors.append(f"manifest row {sid or index}: section_id does not match plot row {row_id}")
        manifest_block = str(_field(manifest, "evidence_block_id", "evidenceBlockId", default="")).strip()
        plot_block = str(_field(plot_row, "evidence_block_id", "evidenceBlockId", default="")).strip()
        if manifest_block != plot_block:
            errors.append(f"manifest row {sid or index}: evidence_block_id does not match plot row {row_id}")
        plot_slide_ids = _values(_field(plot_row, "slide_ids", "slideIds", default=""))
        plot_slide_id = str(_field(plot_row, "slide_id", "slideId", default="")).strip()
        if plot_slide_id:
            plot_slide_ids.append(plot_slide_id)
        if strict and sid and not plot_slide_ids:
            errors.append(f"plot row {row_id}: strict manifest join requires slide_id or slide_ids")
        elif plot_slide_ids and sid and sid not in plot_slide_ids:
            errors.append(f"manifest row {sid}: slide_id is not listed by plot row {row_id}")
        if strict and _values(_field(manifest, "claim_ids", "claimIds", default="")):
            plot_claims = set(_values(_field(plot_row, "claim_refs", "claim_ids", "claimIds", default="")))
            manifest_claims = set(_values(_field(manifest, "claim_ids", "claimIds", default="")))
            if not plot_claims or not manifest_claims <= plot_claims:
                errors.append(f"manifest row {sid}: claim_ids are not covered by plot row {row_id}")
        if strict and _values(_field(manifest, "source_ids", "sourceIds", default="")):
            plot_sources = set(_values(_field(plot_row, "source_refs", "source_ids", "sourceIds", default="")))
            manifest_sources = set(_values(_field(manifest, "source_ids", "sourceIds", default="")))
            if not plot_sources or not manifest_sources <= plot_sources:
                errors.append(f"manifest row {sid}: source_ids are not covered by plot row {row_id}")
        plot_visuals = set(_values(_field(plot_row, "visual_ids", "visualIds", default="")))
        if strict and visual_id and (not plot_visuals or visual_id not in plot_visuals):
            errors.append(f"manifest row {sid}: visual_id={visual_id} is not listed by plot row {row_id}")

    explicit_plot_slides = set()
    explicit_plot_visuals = set()
    for row in rows:
        explicit_plot_slides.update(_values(_field(row, "slide_ids", "slideIds", default="")))
        slide_id = str(_field(row, "slide_id", "slideId", default="")).strip()
        if slide_id:
            explicit_plot_slides.add(slide_id)
        explicit_plot_visuals.update(_values(_field(row, "visual_ids", "visualIds", default="")))
    if strict:
        missing_plot_rows = sorted(set(by_row) - {row_id for row_id in manifest_row_ids if row_id})
        metrics["unjoined_plot_rows"] = len(missing_plot_rows)
        if missing_plot_rows:
            errors.append(f"plot rows are not represented in manifest: {missing_plot_rows[:12]}")
        missing_slides = sorted(explicit_plot_slides - manifest_slide_ids)
        if missing_slides:
            errors.append(f"plot slide_ids are not represented in manifest: {missing_slides[:12]}")
        missing_visuals = sorted(explicit_plot_visuals - manifest_visual_ids)
        if missing_visuals:
            errors.append(f"plot visual_ids are not represented in manifest: {missing_visuals[:12]}")
    return errors, warnings, metrics


def check_plot_file(
    path: Path,
    manifest_rows: list[dict[str, Any]] | None = None,
    *,
    strict: bool = False,
) -> tuple[list[str], list[str], dict[str, Any]]:
    payload, load_errors = _load_payload(path)
    if load_errors:
        return load_errors, [], {"plot_path": str(path)}
    errors, warnings, metrics = check_plot_payload(payload, manifest_rows, strict=strict)
    metrics["plot_path"] = str(path)
    return errors, warnings, metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot", "--storyline-plot", dest="plot", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    rows: list[dict[str, Any]] | None = None
    if args.manifest:
        with args.manifest.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
    errors, warnings, metrics = check_plot_file(args.plot, rows, strict=args.strict)
    report = {"status": "fail" if errors else "pass", "failures": errors, "warnings": warnings, "metrics": metrics}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if args.strict and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
