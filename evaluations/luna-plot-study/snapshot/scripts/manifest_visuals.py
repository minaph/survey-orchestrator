"""Derive per-visual validation views from legacy or nested page manifests."""

from __future__ import annotations

import json
from typing import Any


PAGE_FIELDS = {
    "slide_id", "plot_version", "plot_row_id", "section_id", "evidence_block_id",
    "narrative_job", "evidence_class", "presenter_note", "citation_visible",
    "numeric", "denominator_unit", "aggregation_level", "caveat_visible",
    "min_body_pt", "protected_terms", "internal_vocab_free",
}
PAGE_ALIASES = {
    "slideId": "slide_id", "plotVersion": "plot_version",
    "plotRowId": "plot_row_id", "sectionId": "section_id",
    "evidenceBlockId": "evidence_block_id",
}
VISUAL_FIELDS = {
    "visual_id", "visualId", "kind", "visual_kind", "claim_bearing", "claimBearing",
    "contract_path", "contractPath", "claim_ids", "claimIds", "source_ids", "sourceIds",
    "source_visual_route", "sourceVisualRoute", "route", "primary_visual_type",
    "source_pointer", "figure_id", "figureId", "reader_role", "readerRole", "boundary",
    "status", "semantic_status", "semanticStatus", "semantic_review_status",
    "semanticReviewStatus", "fidelity_status", "fidelityStatus", "visual_review_status",
    "visualReviewStatus", "rights_basis", "rightsBasis", "source_cutout_asset_ids",
    "sourceCutoutAssetIds", "source_cutout_manifest_paths", "sourceCutoutManifestPaths",
    "source_scan_record_paths", "sourceScanRecordPaths", "derived_asset_id", "derivedAssetId",
    "derived_asset_path", "derivedAssetPath", "decision_reason_code", "decisionReasonCode",
    "attribution_note", "attributionNote", "visual_comparison_packet_path",
    "visualComparisonPacketPath", "source_cutout_created_at", "sourceCutoutCreatedAt",
    "reconstruction_created_at", "reconstructionCreatedAt", "generation_id", "generationId",
}


def has_nested_visuals(row: dict[str, Any]) -> bool:
    return "visuals" in row and row["visuals"] != ""


def _nonempty(value: Any) -> bool:
    return value is not None and value != "" and value != []


def expand_manifest_visuals(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Keep legacy rows intact; expand only an explicit nonempty visuals array.

    Page fields are the sole inherited attributes. Source and contract fields
    stay with each child so one figure cannot borrow another figure's joins.
    """
    result: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"manifest row {index}: expected an object")
            continue
        if not has_nested_visuals(row):
            result.append(dict(row))
            continue
        sid = row.get("slide_id", row.get("slideId", index))
        children = row["visuals"]
        if isinstance(children, str):
            try:
                children = json.loads(children)
            except (ValueError, TypeError) as exc:
                errors.append(f"slide {sid}: visuals is not valid JSON: {exc}")
                continue
        if not isinstance(children, list) or not children:
            errors.append(f"slide {sid}: visuals must be a nonempty array")
            continue
        ambiguous = sorted(key for key in VISUAL_FIELDS if _nonempty(row.get(key)))
        if ambiguous:
            errors.append(f"slide {sid}: nested visuals cannot mix with top-level visual fields: {ambiguous}")
        page = {key: row[key] for key in PAGE_FIELDS if key in row}
        for alias, canonical in PAGE_ALIASES.items():
            if alias in row:
                if canonical in page and page[canonical] != row[alias]:
                    errors.append(f"slide {sid}: conflicting page field {canonical}/{alias}")
                else:
                    page[canonical] = row[alias]
        for child_index, child in enumerate(children):
            label = f"slide {sid} visuals[{child_index}]"
            if not isinstance(child, dict):
                errors.append(f"{label}: expected an object")
                continue
            if "visuals" in child:
                errors.append(f"{label}: visuals cannot be nested recursively")
            visual = dict(child)
            for key in ("visual_id", "visualId", "contract_path", "contractPath"):
                if key in child and not isinstance(child[key], str):
                    errors.append(f"{label}: {key} must be a string")
            for alias, canonical in PAGE_ALIASES.items():
                if alias in child:
                    if canonical in child and child[canonical] != child[alias]:
                        errors.append(f"{label}: conflicting child field {canonical}/{alias}")
                    visual[canonical] = child[alias]
                    visual.pop(alias, None)
            for key in PAGE_FIELDS:
                if key in visual and (key not in page or visual[key] != page[key]):
                    errors.append(f"{label}: child cannot override page field {key}")
            visual.update(page)
            result.append(visual)
    seen_ids: set[str] = set()
    for visual in result:
        visual_id = visual.get("visual_id", visual.get("visualId"))
        if isinstance(visual_id, str) and visual_id:
            if visual_id in seen_ids:
                errors.append(f"manifest contains duplicate visual_id={visual_id}")
            seen_ids.add(visual_id)
    return result, errors


def deck_visual_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, str]], list[str]]:
    """Render child JSON scalar/list values in the observer's existing TSV form."""
    records, errors = expand_manifest_visuals(rows)
    result = []
    for record in records:
        converted = {}
        for key, value in record.items():
            if isinstance(value, bool):
                converted[key] = "true" if value else "false"
            elif isinstance(value, list):
                if not all(isinstance(item, str) for item in value):
                    errors.append(f"slide {record.get('slide_id', '?')}: {key} must contain strings")
                converted[key] = "|".join(str(item) for item in value)
            elif value is None:
                converted[key] = ""
            elif isinstance(value, (dict, tuple)):
                errors.append(f"slide {record.get('slide_id', '?')}: unsupported value for {key}")
                converted[key] = ""
            else:
                converted[key] = str(value)
        result.append(converted)
    return result, errors
