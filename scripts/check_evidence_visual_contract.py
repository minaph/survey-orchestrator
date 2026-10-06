#!/usr/bin/env python3
"""Validate claim-bearing evidence-visual contracts.

This is the structured preflight for the four bounded visual kinds described
in references/evidence-visual-contract.md.  It deliberately does not inspect
PPTX/PDF rendering; that remains the responsibility of check_deck_quality.py.

The checker always emits JSON, including for missing or malformed inputs.  In
diagnostic mode it reports failures without making exploratory invocations
fail at the process level.  ``--strict`` turns deterministic failures and
unresolved release states into a non-zero exit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from check_storyline_plot import check_plot_payload
from manifest_visuals import expand_manifest_visuals


SUPPORTED_KINDS = {"table", "diagram", "chart", "source_figure"}
ROUTES = {
    "source_figure",
    "faithful_reconstruction",
    "new_explanatory_visual",
    "no_useful_candidate",
    "inaccessible_source",
    "not_applicable",
}
RECONSTRUCTION_ROUTES = {"faithful_reconstruction", "new_explanatory_visual"}
REASONS = {
    "layout_unreadable",
    "no_source_figure",
    "cross_source_comparison",
    "review_synthesis",
}
REVIEW_STATUSES = {
    "pending",
    "passed",
    "blocked",
    "not_required",
    "not_applicable",
}
RELATIONS = {
    "causal",
    "temporal",
    "classification",
    "reading_order",
    "flow",
    "dependency",
    "comparison",
    "aggregation",
    "other_explicit",
}
URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)
TIMESTAMP_KEYS = ("observed_at", "created_at", "timestamp")
UNESTABLISHED_RIGHTS_BASIS = {"not provided", "unclear"}
_MISSING = object()


class ContractChecker:
    """Small stateful validator whose failures remain JSON-serialisable."""

    def __init__(self, *, strict: bool, audit_root: Path | None, base_dir: Path):
        self.strict = strict
        self.audit_root = audit_root.resolve() if audit_root else None
        self.base_dir = base_dir.resolve()
        self.failures: list[dict[str, Any]] = []
        self.warnings: list[dict[str, Any]] = []
        self.metrics: dict[str, Any] = {}

    def fail(self, code: str, message: str, visual_id: str | None = None) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        if visual_id is not None:
            item["visual_id"] = visual_id
        self.failures.append(item)

    def warn(self, code: str, message: str, visual_id: str | None = None) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        if visual_id is not None:
            item["visual_id"] = visual_id
        self.warnings.append(item)

    def local_path(
        self,
        raw: Any,
        label: str,
        *,
        base: Path | None = None,
        required: bool = True,
        visual_id: str | None = None,
        require_audit_root: bool = False,
    ) -> Path | None:
        """Resolve a local audit path without allowing path escape."""
        if raw is None or raw == "":
            if required:
                self.fail("missing_path", f"{label} is missing", visual_id)
            return None
        if not isinstance(raw, str):
            self.fail("invalid_path_type", f"{label} must be a string path", visual_id)
            return None
        value = raw.strip()
        if not value:
            if required:
                self.fail("missing_path", f"{label} is empty", visual_id)
            return None
        if URL_RE.match(value):
            self.fail("non_local_path", f"{label} must be a local audit path, not a URL", visual_id)
            return None
        if require_audit_root and self.audit_root is None:
            self.fail("audit_root_required", f"--audit-root is required before reading referenced {label}", visual_id)
            return None
        if self.strict and self.audit_root is None:
            self.fail("audit_root_required", f"strict mode requires --audit-root before reading {label}", visual_id)
            return None
        candidate = Path(value)
        candidates = [candidate] if candidate.is_absolute() else []
        if not candidate.is_absolute():
            # Sidecar fields are commonly relative to the sidecar itself,
            # while manifest fields are commonly relative to audit-root.
            # Prefer an existing sidecar-relative path, then audit-root.
            if base is not None:
                candidates.append(base.resolve() / candidate)
            if self.audit_root is not None:
                candidates.append(self.audit_root / candidate)
            if base is None and self.audit_root is None:
                candidates.append(self.base_dir / candidate)
        resolved_candidates: list[Path] = []
        outside = False
        try:
            for item in candidates:
                resolved = item.resolve()
                if self.audit_root is not None:
                    try:
                        resolved.relative_to(self.audit_root)
                    except ValueError:
                        outside = True
                        continue
                resolved_candidates.append(resolved)
        except (OSError, RuntimeError) as exc:
            self.fail("unresolvable_path", f"{label} cannot be resolved: {exc}", visual_id)
            return None
        if not resolved_candidates:
            if outside:
                self.fail("path_outside_audit_root", f"{label} escapes audit-root: {value}", visual_id)
            else:
                self.fail("unresolvable_path", f"{label} has no resolvable local candidate: {value}", visual_id)
            return None
        resolved = next((item for item in resolved_candidates if item.is_file()), resolved_candidates[0])
        if required and not resolved.is_file():
            self.fail("missing_file", f"{label} does not exist: {value}", visual_id)
            return None
        return resolved

    @staticmethod
    def _reject_json_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} is not allowed")

    def load_payload(self, path: Path | None, label: str, visual_id: str | None = None) -> Any:
        if path is None:
            return None
        try:
            if path.suffix.casefold() in {".tsv", ".csv"}:
                delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
                with path.open("r", encoding="utf-8-sig", newline="") as stream:
                    rows = list(csv.DictReader(stream, delimiter=delimiter))
                for index, row in enumerate(rows):
                    if None in row:
                        self.fail("invalid_tsv_shape", f"{label}[{index}] has extra TSV/CSV fields", visual_id)
                if not rows:
                    self.fail("empty_input", f"{label} contains no records", visual_id)
                return rows
            text = path.read_text(encoding="utf-8")
            if not text.strip():
                self.fail("empty_input", f"{label} is empty", visual_id)
                return None
            return json.loads(text, parse_constant=self._reject_json_constant)
        except (OSError, UnicodeError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self.fail("invalid_input", f"{label} is not valid JSON/TSV: {exc}", visual_id)
            return None


def field(record: dict[str, Any], name: str, default: Any = None) -> Any:
    """Read canonical snake_case and the documented camelCase aliases."""
    aliases = {
        "visual_id": ("visual_id", "visualId"),
        "slide_id": ("slide_id", "slideId"),
        "claim_ids": ("claim_ids", "claimIds"),
        "source_ids": ("source_ids", "sourceIds"),
        "source_visual_route": ("source_visual_route", "sourceVisualRoute", "route"),
        "reader_role": ("reader_role", "readerRole"),
        "claim_bearing": ("claim_bearing", "claimBearing"),
        "contract_path": ("contract_path", "contractPath"),
        "source_cutout_asset_ids": ("source_cutout_asset_ids", "sourceCutoutAssetIds"),
        "source_cutout_manifest_paths": ("source_cutout_manifest_paths", "sourceCutoutManifestPaths"),
        "source_scan_record_paths": ("source_scan_record_paths", "sourceScanRecordPaths"),
        "derived_asset_id": ("derived_asset_id", "derivedAssetId"),
        "derived_asset_path": ("derived_asset_path", "derivedAssetPath"),
        "decision_reason_code": ("decision_reason_code", "decisionReasonCode"),
        "visual_comparison_packet_path": ("visual_comparison_packet_path", "visualComparisonPacketPath"),
        "visual_review_status": ("visual_review_status", "visualReviewStatus"),
        "semantic_status": ("semantic_status", "semanticStatus", "semantic_review_status", "semanticReviewStatus"),
        "fidelity_status": ("fidelity_status", "fidelityStatus"),
        "deterministic_status": ("deterministic_status", "deterministicStatus"),
        "source_cutout_created_at": ("source_cutout_created_at", "sourceCutoutCreatedAt"),
        "reconstruction_created_at": ("reconstruction_created_at", "reconstructionCreatedAt"),
        "rights_basis": ("rights_basis", "rightsBasis"),
        "attribution_note": ("attribution_note", "attributionNote"),
        "figure_id": ("figure_id", "figureId"),
        "generation_id": ("generation_id", "generationId"),
    }
    for key in aliases.get(name, (name,)):
        if key in record:
            return record[key]
    return default


def records_from_payload(payload: Any, keys: tuple[str, ...], label: str, checker: ContractChecker) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = None
        for key in keys:
            candidate = payload.get(key)
            if isinstance(candidate, list):
                records = candidate
                break
        if records is None:
            # A single contract/record object is a valid envelope. A manifest
            # or ledger without its expected collection is not.
            if any(key in payload for key in ("visual_id", "visualId", "claim_id", "source_id", "asset_id")):
                records = [payload]
            else:
                checker.fail("missing_collection", f"{label} lacks one of {list(keys)}")
                return []
    else:
        checker.fail("invalid_collection", f"{label} must be a JSON object or array")
        return []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            checker.fail("invalid_record", f"{label}[{index}] must be an object")
        else:
            result.append(item)
    if not result:
        checker.fail("empty_collection", f"{label} contains no records")
    return result


def string_value(value: Any, label: str, checker: ContractChecker, visual_id: str | None = None, *, required: bool = False) -> str:
    if value is None:
        if required:
            checker.fail("missing_string", f"{label} is missing", visual_id)
        return ""
    if not isinstance(value, str):
        checker.fail("invalid_string_type", f"{label} must be a string", visual_id)
        return ""
    result = value.strip()
    if required and not result:
        checker.fail("missing_string", f"{label} is empty", visual_id)
    return result


def string_array(
    value: Any,
    label: str,
    checker: ContractChecker,
    visual_id: str | None = None,
    *,
    required: bool = False,
) -> list[str]:
    """Read a semantic string array without accepting TSV-style delimiters."""
    if value is None:
        if required:
            checker.fail("missing_string_array", f"{label} is missing", visual_id)
        return []
    if not isinstance(value, list):
        checker.fail("invalid_string_array_type", f"{label} must be an array of strings", visual_id)
        return []
    values: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            checker.fail("invalid_string_array_item", f"{label}[{index}] must be a string", visual_id)
            continue
        item = item.strip()
        if item:
            values.append(item)
    if required and not values:
        checker.fail("missing_string_array", f"{label} is empty", visual_id)
    if len(values) != len(set(values)):
        checker.fail("duplicate_join_key", f"{label} contains duplicate values", visual_id)
    return values


def boolean_value(value: Any, label: str, checker: ContractChecker, visual_id: str | None = None) -> bool | None:
    """Accept JSON booleans and the exact textual booleans emitted by TSV."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"true", "yes", "1"}:
            return True
        if normalized in {"false", "no", "0"}:
            return False
    checker.fail("invalid_boolean_type", f"{label} must be a boolean or exact TSV boolean token", visual_id)
    return None


def string_list(
    value: Any,
    label: str,
    checker: ContractChecker,
    visual_id: str | None = None,
    *,
    required: bool = False,
    allow_comma: bool = False,
) -> list[str]:
    if value is None:
        if required:
            checker.fail("missing_string_list", f"{label} is missing", visual_id)
        return []
    if isinstance(value, str):
        # TSV manifests use pipe-separated fields. Some legacy ledgers use
        # comma-separated IDs; allow that only at explicit identifier joins.
        delimiter = r"[|,]" if allow_comma else r"[|]"
        values = [part.strip() for part in re.split(delimiter, value) if part.strip()]
    elif isinstance(value, list):
        values = []
        for index, item in enumerate(value):
            if not isinstance(item, str):
                checker.fail("invalid_join_key_type", f"{label}[{index}] must be a string", visual_id)
                continue
            if item.strip():
                values.append(item.strip())
    else:
        checker.fail("invalid_string_list_type", f"{label} must be a list of strings", visual_id)
        return []
    if required and not values:
        checker.fail("missing_string_list", f"{label} is empty", visual_id)
    if len(values) != len(set(values)):
        checker.fail("duplicate_join_key", f"{label} contains duplicate values", visual_id)
    return values


def finite_number(value: Any) -> bool:
    """Check numeric finiteness without converting arbitrary-size integers."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if isinstance(value, int):
        # Python integers are arbitrary precision and are finite by definition.
        return True
    try:
        return math.isfinite(value)
    except (OverflowError, TypeError, ValueError):
        return False


def valid_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except (TypeError, ValueError, OverflowError):
        return None
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)


def resolve_record_path(checker: ContractChecker, raw: Any, label: str, visual_id: str | None, *, base: Path | None = None) -> Path | None:
    path = checker.local_path(raw, label, base=base, required=True, visual_id=visual_id, require_audit_root=True)
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_table(semantics: dict[str, Any], checker: ContractChecker, visual_id: str) -> None:
    row_axis = semantics.get("row_axis", semantics.get("rowAxis"))
    col_axis = semantics.get("column_axis", semantics.get("columnAxis"))
    if not isinstance(row_axis, dict):
        checker.fail("table_row_axis_missing", "table row_axis must be an object", visual_id)
        row_axis = {}
    if not isinstance(col_axis, dict):
        checker.fail("table_column_axis_missing", "table column_axis must be an object", visual_id)
        col_axis = {}
    row_name = string_value(row_axis.get("name"), "table row_axis.name", checker, visual_id, required=True)
    row_meaning = string_value(row_axis.get("meaning"), "table row_axis.meaning", checker, visual_id, required=True)
    col_name = string_value(col_axis.get("name"), "table column_axis.name", checker, visual_id, required=True)
    col_meaning = string_value(col_axis.get("meaning"), "table column_axis.meaning", checker, visual_id, required=True)
    rows = string_array(row_axis.get("labels"), "table row_axis.labels", checker, visual_id, required=True)
    cols = string_array(col_axis.get("labels"), "table column_axis.labels", checker, visual_id, required=True)
    cell_meaning = string_value(semantics.get("cell_meaning", semantics.get("cellMeaning")), "table cell_meaning", checker, visual_id, required=True)
    orientation = string_value(semantics.get("orientation"), "table orientation", checker, visual_id, required=True)
    axis_mirror = string_value(semantics.get("axis_mirror", semantics.get("axisMirror")), "table axis_mirror", checker, visual_id, required=True)
    expected_mirror = (
        f"rows = {row_meaning}; columns = {col_meaning}; cell = {cell_meaning}; orientation = {orientation}"
    )
    if axis_mirror and axis_mirror != expected_mirror:
        checker.fail("table_axis_mirror_mismatch", "table axis_mirror must be generated from the declared axis/cell meanings", visual_id)
    _ = row_name, col_name
    string_value(semantics.get("unit"), "table unit", checker, visual_id, required=True)
    cells = semantics.get("cells")
    if not isinstance(cells, list):
        checker.fail("table_cells_missing", "table cells must be a matrix or cell list", visual_id)
        return
    if cells and all(isinstance(item, dict) for item in cells):
        expected = {(row, col) for row in rows for col in cols}
        seen: set[tuple[str, str]] = set()
        for index, cell in enumerate(cells):
            row = string_value(cell.get("row", cell.get("row_id")), f"table cells[{index}].row", checker, visual_id, required=True)
            col = string_value(cell.get("column", cell.get("column_id")), f"table cells[{index}].column", checker, visual_id, required=True)
            pair = (row, col)
            if pair not in expected:
                checker.fail("table_unknown_cell", f"table cell coordinate is not declared: {pair}", visual_id)
            if pair in seen:
                checker.fail("table_duplicate_cell", f"table cell coordinate is duplicated: {pair}", visual_id)
            seen.add(pair)
            if "value" in cell and isinstance(cell["value"], (int, float, bool)) and not finite_number(cell["value"]):
                checker.fail("table_invalid_numeric_cell", f"table cell {pair} is not finite", visual_id)
        if seen != expected:
            checker.fail("table_cartesian_coverage", "table cells do not cover the declared row x column Cartesian product", visual_id)
        return
    if len(cells) != len(rows):
        checker.fail("table_row_count", f"table has {len(cells)} cell rows but declares {len(rows)} row labels", visual_id)
    for index, row in enumerate(cells):
        if not isinstance(row, list):
            checker.fail("table_row_shape", f"table cells[{index}] must be a list", visual_id)
            continue
        if len(row) != len(cols):
            checker.fail("table_column_count", f"table cells[{index}] has {len(row)} cells but declares {len(cols)} columns", visual_id)
        for col_index, value in enumerate(row):
            if isinstance(value, (int, float, bool)) and not finite_number(value):
                checker.fail("table_invalid_numeric_cell", f"table cell [{index},{col_index}] is not finite", visual_id)


def check_diagram(semantics: dict[str, Any], checker: ContractChecker, visual_id: str) -> None:
    nodes = semantics.get("nodes")
    edges = semantics.get("edges")
    if not isinstance(nodes, list) or not nodes:
        checker.fail("diagram_nodes_missing", "diagram nodes must be a non-empty list", visual_id)
        nodes = []
    node_ids: list[str] = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            checker.fail("diagram_node_shape", f"diagram nodes[{index}] must be an object", visual_id)
            continue
        node_id = string_value(node.get("id"), f"diagram nodes[{index}].id", checker, visual_id, required=True)
        if node_id:
            node_ids.append(node_id)
        string_value(node.get("meaning"), f"diagram nodes[{index}].meaning", checker, visual_id, required=True)
    if len(node_ids) != len(set(node_ids)):
        checker.fail("diagram_duplicate_node", "diagram node IDs must be unique", visual_id)
    node_set = set(node_ids)
    if not isinstance(edges, list):
        checker.fail("diagram_edges_missing", "diagram edges must be a list", visual_id)
        edges = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            checker.fail("diagram_edge_shape", f"diagram edges[{index}] must be an object", visual_id)
            continue
        source = string_value(edge.get("from", edge.get("source")), f"diagram edges[{index}].from", checker, visual_id, required=True)
        target = string_value(edge.get("to", edge.get("target")), f"diagram edges[{index}].to", checker, visual_id, required=True)
        relation = string_value(edge.get("relation", edge.get("relation_type", edge.get("relationType"))), f"diagram edges[{index}].relation", checker, visual_id, required=True)
        if source and source not in node_set:
            checker.fail("diagram_unknown_endpoint", f"diagram edge source is undeclared: {source}", visual_id)
        if target and target not in node_set:
            checker.fail("diagram_unknown_endpoint", f"diagram edge target is undeclared: {target}", visual_id)
        if relation and relation not in RELATIONS:
            checker.fail("diagram_invalid_relation", f"diagram edge relation is not in the controlled vocabulary: {relation}", visual_id)
    reading_order = semantics.get("reading_order", semantics.get("readingOrder"))
    if reading_order is None:
        checker.fail("diagram_reading_order_missing", "diagram reading_order is required", visual_id)
    else:
        order = string_array(reading_order, "diagram reading_order", checker, visual_id, required=True)
        if set(order) != node_set or len(order) != len(node_ids):
            checker.fail("diagram_reading_order", "diagram reading_order must name each declared node exactly once", visual_id)
    has_visual_encoding = any(
        isinstance(node, dict) and any(key in node for key in ("color", "fill", "line_style", "shape", "position", "x", "y"))
        for node in nodes
    ) or any(
        isinstance(edge, dict) and any(key in edge for key in ("color", "line_style", "style"))
        for edge in edges
    )
    legend = semantics.get("legend")
    if has_visual_encoding and not string_value(legend, "diagram legend", checker, visual_id, required=True):
        pass


def axis_object(value: Any, label: str, checker: ContractChecker, visual_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        checker.fail("chart_axis_missing", f"{label} must be an object", visual_id)
        return {}
    string_value(value.get("name"), f"{label}.name", checker, visual_id, required=True)
    string_value(value.get("unit"), f"{label}.unit", checker, visual_id, required=True)
    return value


def check_chart(semantics: dict[str, Any], checker: ContractChecker, visual_id: str) -> None:
    x_axis = axis_object(semantics.get("x_axis", semantics.get("xAxis")), "chart x_axis", checker, visual_id)
    y_axis = axis_object(semantics.get("y_axis", semantics.get("yAxis")), "chart y_axis", checker, visual_id)
    _ = x_axis, y_axis
    comparator = string_value(semantics.get("comparator"), "chart comparator", checker, visual_id, required=True)
    if comparator == "none_applicable":
        string_value(
            semantics.get("comparator_explanation", semantics.get("comparatorExplanation")),
            "chart comparator_explanation",
            checker,
            visual_id,
            required=True,
        )
    string_value(semantics.get("aggregation"), "chart aggregation", checker, visual_id, required=True)
    domain = semantics.get("domain")
    if domain is None:
        checker.fail("chart_domain_missing", "chart domain is required", visual_id)
        return
    if not isinstance(domain, dict):
        checker.fail("chart_domain_shape", "chart domain must be an object", visual_id)
        return
    domain_type = string_value(domain.get("type", semantics.get("domain_type")), "chart domain.type", checker, visual_id, required=True).lower()
    if domain_type in {"continuous", "log"}:
        if "min" not in domain or "max" not in domain:
            checker.fail("chart_domain_bounds", "continuous/log chart domain requires finite min and max", visual_id)
        else:
            low, high = domain.get("min"), domain.get("max")
            low_valid = finite_number(low)
            high_valid = finite_number(high)
            if not low_valid:
                checker.fail("invalid_numeric_domain", "chart domain.min must be one finite numeric scalar (not bool/NaN/Inf/list/object)", visual_id)
            if not high_valid:
                checker.fail("invalid_numeric_domain", "chart domain.max must be one finite numeric scalar (not bool/NaN/Inf/list/object)", visual_id)
            if low_valid and high_valid:
                try:
                    if low >= high:
                        checker.fail("chart_domain_order", "chart domain requires min < max", visual_id)
                except (TypeError, OverflowError):
                    checker.fail("chart_domain_order", "chart domain bounds cannot be compared safely", visual_id)
                if domain_type == "log" and (not finite_number(low) or low <= 0):
                    checker.fail("chart_log_domain", "log chart domain requires a positive min", visual_id)
    elif domain_type in {"category", "categorical"}:
        labels = domain.get("labels", domain.get("values"))
        string_array(labels, "chart domain.labels", checker, visual_id, required=True)
    else:
        checker.fail("chart_domain_type", "chart domain.type must be continuous, log, category, or categorical", visual_id)
    uncertainty = semantics.get("uncertainty")
    if uncertainty is not None:
        string_value(uncertainty, "chart uncertainty", checker, visual_id, required=True)


def contract_semantics(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("semantics")
    return value if isinstance(value, dict) else {}


def check_review_status(value: Any, label: str, checker: ContractChecker, visual_id: str) -> str:
    if value is None or value == "":
        return ""
    status = string_value(value, label, checker, visual_id).lower()
    if status and status not in REVIEW_STATUSES:
        checker.fail("invalid_review_status", f"{label} must be one of {sorted(REVIEW_STATUSES)}", visual_id)
    return status


def status_from_contract(contract: dict[str, Any], name: str) -> str:
    direct = field(contract, name)
    if direct is not None:
        return str(direct).strip().lower() if isinstance(direct, str) else ""
    nested = contract.get("review")
    if isinstance(nested, dict):
        camel = {
            "deterministic_status": "deterministicStatus",
            "semantic_status": "semanticStatus",
            "fidelity_status": "fidelityStatus",
            "visual_review_status": "visualReviewStatus",
        }.get(name, name)
        value = nested.get(name, nested.get(camel))
        return value.strip().lower() if isinstance(value, str) else ""
    return ""


def check_contract_review(
    checker: ContractChecker,
    visual: dict[str, Any],
    contract: dict[str, Any],
    visual_id: str,
) -> dict[str, str]:
    """Validate the common nested review state and its manifest aliases."""
    review = contract.get("review")
    if not isinstance(review, dict):
        checker.fail("review_missing", "claim-bearing contract requires review={deterministic_status, semantic_status, fidelity_status}", visual_id)
        review = {}
    statuses: dict[str, str] = {}
    for name in ("deterministic_status", "semantic_status", "fidelity_status"):
        camel = {
            "deterministic_status": "deterministicStatus",
            "semantic_status": "semanticStatus",
            "fidelity_status": "fidelityStatus",
        }[name]
        nested = check_review_status(review.get(name, review.get(camel)), f"contract.review.{name}", checker, visual_id)
        if not nested:
            checker.fail("review_status_missing", f"contract.review.{name} is required", visual_id)
        statuses[name] = nested
        direct_value = field(contract, name)
        if direct_value is None and name != "deterministic_status":
            direct_value = field(visual, name)
        direct = check_review_status(direct_value, f"manifest/contract.{name}", checker, visual_id)
        if direct and nested and direct != nested:
            checker.fail("review_status_join", f"flat {name} does not match contract.review.{name}", visual_id)
        if name != "deterministic_status" and not direct:
            checker.fail("manifest_review_status_missing", f"manifest/contract {name} join value is required", visual_id)
    if checker.strict and statuses.get("deterministic_status") != "passed":
        checker.fail("deterministic_review_pending", "contract.review.deterministic_status must be passed in strict mode", visual_id)
    return statuses


def check_structured_record(
    checker: ContractChecker,
    raw_path: Any,
    label: str,
    expected: str,
    visual_id: str,
    expected_source_ids: set[str],
    expected_generation_id: str = "",
) -> tuple[Path | None, datetime | None]:
    path = resolve_record_path(checker, raw_path, label, visual_id)
    if path is None:
        return None, None
    payload = checker.load_payload(path, label, visual_id)
    if isinstance(payload, list):
        if not all(isinstance(item, dict) for item in payload):
            checker.fail("invalid_audit_record", f"{label} collection contains a non-object record", visual_id)
            return path, None
        if len(payload) != 1:
            checker.fail(
                "audit_record_visual_join",
                f"{label} must contain exactly one per-visual record, not a shared collection",
                visual_id,
            )
            return path, None
        payload = payload[0]
    if not isinstance(payload, dict):
        checker.fail("invalid_audit_record", f"{label} must be a JSON object or visual-keyed collection", visual_id)
        return path, None
    record_type = string_value(payload.get("record_type"), f"{label}.record_type", checker, visual_id, required=True)
    status = string_value(payload.get("status"), f"{label}.status", checker, visual_id, required=True).lower()
    route = string_value(payload.get("source_visual_route"), f"{label}.source_visual_route", checker, visual_id, required=True)
    locator = payload.get("locator", payload.get("source_locator", payload.get("access_locator")))
    string_value(locator, f"{label}.locator", checker, visual_id, required=True)
    if expected == "no_useful_candidate":
        if record_type != "source_figure_scan":
            checker.fail("invalid_scan_record_type", f"{label} must declare record_type=source_figure_scan", visual_id)
        if route != "no_useful_candidate":
            checker.fail("scan_route_mismatch", f"{label} must declare source_visual_route=no_useful_candidate", visual_id)
        if status != "no_candidate":
            checker.fail("scan_status_mismatch", f"{label} must declare status=no_candidate", visual_id)
        string_value(payload.get("reason", payload.get("summary", payload.get("note"))), f"{label}.reason", checker, visual_id, required=True)
    else:
        if record_type != "source_figure_access":
            checker.fail("invalid_access_record_type", f"{label} must declare record_type=source_figure_access", visual_id)
        if route != "inaccessible_source":
            checker.fail("access_route_mismatch", f"{label} must declare source_visual_route=inaccessible_source", visual_id)
        if status != "inaccessible":
            checker.fail("access_status_mismatch", f"{label} must declare status=inaccessible", visual_id)
        string_value(payload.get("access_status"), f"{label}.access_status", checker, visual_id, required=True)
    source_id = payload.get("source_id")
    if source_id is not None:
        source_id_value = string_value(source_id, f"{label}.source_id", checker, visual_id, required=True)
        if expected_source_ids and source_id_value not in expected_source_ids:
            checker.fail("audit_record_source_join", f"{label}.source_id is not joined to the manifest", visual_id)
    elif expected_source_ids:
        checker.fail("audit_record_source_join", f"{label}.source_id is required when the visual declares source_ids", visual_id)
    raw_record_visual_id = field(payload, "visual_id", _MISSING)
    if raw_record_visual_id is _MISSING or raw_record_visual_id is None:
        checker.fail("audit_record_visual_join", f"{label}.visual_id is required for a per-visual record", visual_id)
        record_visual_id = ""
    else:
        record_visual_id = string_value(raw_record_visual_id, f"{label}.visual_id", checker, visual_id, required=True)
    if record_visual_id and record_visual_id != visual_id:
        checker.fail("audit_record_visual_join", f"{label}.visual_id does not match the visual", visual_id)
    if expected_generation_id:
        record_generation_id = string_value(
            field(payload, "generation_id"),
            f"{label}.generation_id",
            checker,
            visual_id,
            required=True,
        )
        if record_generation_id != expected_generation_id:
            checker.fail("audit_record_generation_join", f"{label}.generation_id does not match the visual generation", visual_id)
    elif field(payload, "generation_id", _MISSING) not in (_MISSING, None, ""):
        checker.fail("generation_join", f"{label}.generation_id is present but not joined to manifest/contract generation_id", visual_id)
    observed = None
    for key in TIMESTAMP_KEYS:
        if payload.get(key) is not None:
            observed = valid_timestamp(payload.get(key))
            if observed is None:
                checker.fail("invalid_timestamp", f"{label}.{key} is not an ISO timestamp", visual_id)
            break
    if observed is None:
        checker.fail("missing_timestamp", f"{label} requires observed_at/created_at/timestamp", visual_id)
    return path, observed


def check_source_cutout(
    checker: ContractChecker,
    raw_path: Any,
    expected_asset_id: str,
    visual_id: str,
    expected_claim_ids: set[str],
    expected_source_ids: set[str],
    expected_figure_id: str,
    expected_fidelity_status: str,
    expected_rights_basis: str,
    expected_generation_id: str = "",
) -> None:
    path = resolve_record_path(checker, raw_path, "source-cutout manifest", visual_id)
    if path is None:
        return
    payload = checker.load_payload(path, "source-cutout manifest", visual_id)
    if not isinstance(payload, dict):
        checker.fail("invalid_source_cutout", "source-cutout manifest must be a JSON object", visual_id)
        return
    asset_id = string_value(payload.get("asset_id"), "source-cutout asset_id", checker, visual_id, required=True)
    if asset_id != expected_asset_id:
        checker.fail("source_cutout_asset_join", "source-cutout asset_id does not match the visual", visual_id)
    raw_record_visual_id = field(payload, "visual_id", _MISSING)
    if raw_record_visual_id is _MISSING or raw_record_visual_id is None:
        checker.fail("source_cutout_visual_join", "source-cutout visual_id is required for a per-visual sidecar", visual_id)
        record_visual_id = ""
    else:
        record_visual_id = string_value(raw_record_visual_id, "source-cutout visual_id", checker, visual_id, required=True)
    if record_visual_id and record_visual_id != visual_id:
        checker.fail("source_cutout_visual_join", "source-cutout visual_id does not match the visual", visual_id)
    if expected_generation_id:
        record_generation_id = string_value(
            field(payload, "generation_id"),
            "source-cutout generation_id",
            checker,
            visual_id,
            required=True,
        )
        if record_generation_id != expected_generation_id:
            checker.fail("source_cutout_generation_join", "source-cutout generation_id does not match the visual generation", visual_id)
    elif field(payload, "generation_id", _MISSING) not in (_MISSING, None, ""):
        checker.fail("generation_join", "source-cutout generation_id is present but not joined to manifest/contract generation_id", visual_id)
    if payload.get("asset_role") != "source_cutout":
        checker.fail("source_cutout_role", "source-cutout manifest must declare asset_role=source_cutout", visual_id)
    if payload.get("review_only") is not True:
        checker.fail("source_cutout_review_only", "source-cutout manifest must declare review_only=true", visual_id)
    figure_id = string_value(payload.get("figure_id"), "source-cutout figure_id", checker, visual_id, required=True)
    if expected_figure_id and figure_id != expected_figure_id:
        checker.fail("source_cutout_figure_join", "source-cutout figure_id does not match the visual contract", visual_id)
    sidecar_rights_basis = string_value(payload.get("rights_basis"), "source-cutout rights_basis", checker, visual_id, required=True)
    if expected_rights_basis and sidecar_rights_basis != expected_rights_basis:
        checker.fail("source_cutout_rights_join", "source-cutout rights_basis does not match the visual contract", visual_id)
    sidecar_fidelity = check_review_status(payload.get("fidelity_status"), "source-cutout fidelity_status", checker, visual_id)
    if not sidecar_fidelity:
        checker.fail("source_cutout_fidelity_missing", "source-cutout fidelity_status is required", visual_id)
    if expected_fidelity_status and sidecar_fidelity and sidecar_fidelity != expected_fidelity_status:
        checker.fail("source_cutout_fidelity_join", "source-cutout fidelity_status does not match the visual contract", visual_id)
    if checker.strict and sidecar_fidelity not in {"passed", "not_required"}:
        checker.fail("source_cutout_fidelity_pending", "source-cutout fidelity_status must be passed or not_required in strict mode", visual_id)
    claim_ids = set(string_list(payload.get("claim_ids"), "source-cutout claim_ids", checker, visual_id, required=True, allow_comma=True))
    if expected_claim_ids and not expected_claim_ids.intersection(claim_ids):
        checker.fail("source_cutout_claim_join", "source-cutout has no claim join with the visual", visual_id)
    source_id = string_value(payload.get("source_id"), "source-cutout source_id", checker, visual_id, required=True)
    if expected_source_ids and source_id not in expected_source_ids:
        checker.fail("source_cutout_source_join", "source-cutout source_id is not joined to the visual", visual_id)
    source_hash = string_value(payload.get("source_sha256"), "source-cutout source_sha256", checker, visual_id, required=True)
    output_hash = string_value(payload.get("output_sha256"), "source-cutout output_sha256", checker, visual_id, required=True)
    for hash_value, label in ((source_hash, "source-cutout source_sha256"), (output_hash, "source-cutout output_sha256")):
        if hash_value and not re.fullmatch(r"[0-9a-fA-F]{64}", hash_value):
            checker.fail("invalid_sha256", f"{label} must be a 64-character hexadecimal SHA-256", visual_id)
    hash_basis = string_value(payload.get("source_hash_basis"), "source-cutout source_hash_basis", checker, visual_id, required=True)
    output_raw = payload.get("output")
    output_path = resolve_record_path(checker, output_raw, "source-cutout output", visual_id, base=path.parent)
    if output_path is not None:
        try:
            if sha256_file(output_path).casefold() != output_hash.casefold():
                checker.fail("source_cutout_output_hash", "source-cutout output_sha256 does not match the file", visual_id)
        except (OSError, ValueError) as exc:
            checker.fail("source_cutout_hash_error", f"source-cutout output hash could not be read: {exc}", visual_id)
    source_material = payload.get("source_snapshot_path") or payload.get("local_image_path") or payload.get("local_source_path")
    if source_material:
        source_path = resolve_record_path(checker, source_material, "source-cutout source material", visual_id, base=path.parent)
        if source_path is not None and source_hash:
            try:
                if sha256_file(source_path).casefold() != source_hash.casefold():
                    checker.fail("source_cutout_source_hash", "source_sha256 does not match the source material", visual_id)
            except (OSError, ValueError) as exc:
                checker.fail("source_cutout_hash_error", f"source hash could not be read: {exc}", visual_id)
    elif checker.strict:
        source_locator = payload.get("canonical_url_or_doi") or payload.get("source_url_or_doi")
        if hash_basis.casefold() in {"local_source_file", "local_image_file", "local_pdf"} or not isinstance(source_locator, str) or not source_locator.strip():
            checker.fail("source_material_missing", "strict source-cutout release needs a local source material path or a URL/DOI-backed hash basis", visual_id)


def check_packet(
    checker: ContractChecker,
    raw_path: Any,
    visual_id: str,
    source_cutout_ids: set[str],
    derived_asset_id: str,
    claim_ids: set[str],
    reason: str,
    review_status: str,
    expected_generation_id: str = "",
) -> None:
    path = resolve_record_path(checker, raw_path, "visual comparison packet", visual_id)
    if path is None:
        return
    payload = checker.load_payload(path, "visual comparison packet", visual_id)
    if not isinstance(payload, dict):
        checker.fail("invalid_comparison_packet", "visual comparison packet must be a JSON object", visual_id)
        return
    raw_record_visual_id = field(payload, "visual_id", _MISSING)
    if raw_record_visual_id is _MISSING or raw_record_visual_id is None:
        checker.fail("comparison_visual_join", "comparison packet visual_id is required for a per-visual packet", visual_id)
        record_visual_id = ""
    else:
        record_visual_id = string_value(raw_record_visual_id, "comparison packet visual_id", checker, visual_id, required=True)
    if record_visual_id and record_visual_id != visual_id:
        checker.fail("comparison_visual_join", "comparison packet visual_id does not match the visual", visual_id)
    if expected_generation_id:
        record_generation_id = string_value(
            field(payload, "generation_id"),
            "comparison packet generation_id",
            checker,
            visual_id,
            required=True,
        )
        if record_generation_id != expected_generation_id:
            checker.fail("comparison_generation_join", "comparison packet generation_id does not match the visual generation", visual_id)
    elif field(payload, "generation_id", _MISSING) not in (_MISSING, None, ""):
        checker.fail("generation_join", "comparison packet generation_id is present but not joined to manifest/contract generation_id", visual_id)
    if set(string_list(payload.get("source_cutout_asset_ids"), "comparison packet source_cutout_asset_ids", checker, visual_id, allow_comma=True)) != source_cutout_ids:
        checker.fail("comparison_source_join", "comparison packet source-cutout IDs do not match the visual", visual_id)
    if string_value(payload.get("derived_asset_id"), "comparison packet derived_asset_id", checker, visual_id, required=True) != derived_asset_id:
        checker.fail("comparison_derived_join", "comparison packet derived_asset_id does not match the visual", visual_id)
    if set(string_list(payload.get("claim_ids"), "comparison packet claim_ids", checker, visual_id, allow_comma=True)) != claim_ids:
        checker.fail("comparison_claim_join", "comparison packet claim IDs do not match the visual", visual_id)
    if string_value(payload.get("decision_reason_code"), "comparison packet decision_reason_code", checker, visual_id, required=True) != reason:
        checker.fail("comparison_reason_join", "comparison packet decision reason does not match the visual", visual_id)
    packet_status = string_value(payload.get("visual_review_status"), "comparison packet visual_review_status", checker, visual_id, required=True).lower()
    if packet_status != review_status:
        checker.fail("comparison_status_join", "comparison packet review status does not match the visual", visual_id)
    for key in ("preserved_relation", "changed_elements", "added_interpretation"):
        string_value(
            payload.get(key),
            f"comparison packet {key}",
            checker,
            visual_id,
            required=True,
        )
    if checker.strict and packet_status != "passed":
        checker.fail("comparison_not_passed", "comparison packet must be passed in strict mode", visual_id)


def visual_asset_ids(contract: dict[str, Any]) -> list[str]:
    ids = string_list(field(contract, "source_cutout_asset_ids"), "source_cutout_asset_ids", _NullChecker(), allow_comma=True)
    derived = field(contract, "derived_asset_id")
    if isinstance(derived, str) and derived.strip():
        ids.append(derived.strip())
    return ids


class _NullChecker:
    """Adapter used only to reuse string_list for non-reporting collection."""

    def fail(self, *_args: Any, **_kwargs: Any) -> None:
        return None


def route_list_field(
    record: dict[str, Any],
    name: str,
    label: str,
    checker: ContractChecker,
    visual_id: str,
    *,
    allow_empty: bool,
) -> list[str]:
    """Read a route field while preserving the distinction between absent and empty."""
    raw = field(record, name, _MISSING)
    if raw is _MISSING or raw is None:
        checker.fail("route_field_missing", f"{label} must be declared on both manifest and contract", visual_id)
        return []
    return string_list(
        raw,
        label,
        checker,
        visual_id,
        required=not allow_empty,
        allow_comma=name.endswith("_ids"),
    )


def route_scalar_field(
    record: dict[str, Any],
    name: str,
    label: str,
    checker: ContractChecker,
    visual_id: str,
    *,
    required: bool,
) -> str:
    raw = field(record, name, _MISSING)
    if raw is _MISSING or raw is None:
        if required:
            checker.fail("route_field_missing", f"{label} must be declared on both manifest and contract", visual_id)
        return ""
    return string_value(raw, label, checker, visual_id, required=required)


def check_route_manifest_contract_join(
    checker: ContractChecker,
    visual: dict[str, Any],
    contract: dict[str, Any],
    visual_id: str,
    route: str,
    reason: str,
) -> str:
    """Join conditional provenance fields before route evidence is consumed.

    The generation identifier is deliberately optional: projects may use
    explicit IDs/hashes without promoting review-round history to a universal
    schema. When supplied, however, it must be present and equal in every
    declaration that claims that generation.
    """
    if route not in ROUTES or route == "not_applicable":
        return ""

    list_specs: list[tuple[str, bool, bool]] = []
    required_scalars: list[str] = []
    optional_scalars: list[str] = []
    if route == "source_figure":
        list_specs = [
            ("source_ids", False, True),
            ("claim_ids", False, True),
            ("source_cutout_asset_ids", False, True),
            ("source_cutout_manifest_paths", False, False),
            ("source_scan_record_paths", True, False),
        ]
        required_scalars = ["figure_id", "rights_basis", "source_cutout_created_at"]
    elif route in RECONSTRUCTION_ROUTES:
        no_source = reason == "no_source_figure"
        list_specs = [
            ("source_ids", no_source, True),
            ("claim_ids", False, True),
            ("source_cutout_asset_ids", no_source, True),
            ("source_cutout_manifest_paths", no_source, False),
            ("source_scan_record_paths", not no_source, False),
        ]
        required_scalars = [
            "derived_asset_id",
            "derived_asset_path",
            "decision_reason_code",
            "attribution_note",
            "visual_comparison_packet_path",
            "reconstruction_created_at",
        ]
        if not no_source:
            required_scalars.extend(["figure_id", "rights_basis", "source_cutout_created_at"])
        if no_source:
            optional_scalars.append("source_cutout_created_at")
    elif route == "no_useful_candidate":
        list_specs = [
            ("source_ids", True, True),
            ("claim_ids", False, True),
            ("source_cutout_asset_ids", True, True),
            ("source_cutout_manifest_paths", True, False),
            ("source_scan_record_paths", False, False),
        ]
        required_scalars = ["decision_reason_code"]
    elif route == "inaccessible_source":
        list_specs = [
            ("source_ids", False, True),
            ("claim_ids", False, True),
            ("source_cutout_asset_ids", True, True),
            ("source_cutout_manifest_paths", True, False),
            ("source_scan_record_paths", False, False),
        ]

    for name, allow_empty, compare_as_set in list_specs:
        manifest_values = route_list_field(
            visual,
            name,
            f"manifest.{name}",
            checker,
            visual_id,
            allow_empty=allow_empty,
        )
        contract_values = route_list_field(
            contract,
            name,
            f"contract.{name}",
            checker,
            visual_id,
            allow_empty=allow_empty,
        )
        left = set(manifest_values) if compare_as_set else manifest_values
        right = set(contract_values) if compare_as_set else contract_values
        if left != right:
            checker.fail("route_field_join", f"manifest.{name} does not match contract.{name}", visual_id)

    for name in required_scalars:
        manifest_value = route_scalar_field(visual, name, f"manifest.{name}", checker, visual_id, required=True)
        contract_value = route_scalar_field(contract, name, f"contract.{name}", checker, visual_id, required=True)
        if manifest_value and contract_value and manifest_value != contract_value:
            checker.fail("route_field_join", f"manifest.{name} does not match contract.{name}", visual_id)

    for name in optional_scalars:
        manifest_value = route_scalar_field(visual, name, f"manifest.{name}", checker, visual_id, required=False)
        contract_value = route_scalar_field(contract, name, f"contract.{name}", checker, visual_id, required=False)
        if manifest_value or contract_value:
            if not manifest_value or not contract_value or manifest_value != contract_value:
                checker.fail("route_field_join", f"manifest.{name} does not match contract.{name}", visual_id)

    manifest_generation = route_scalar_field(visual, "generation_id", "manifest.generation_id", checker, visual_id, required=False)
    contract_generation = route_scalar_field(contract, "generation_id", "contract.generation_id", checker, visual_id, required=False)
    if manifest_generation or contract_generation:
        if not manifest_generation or not contract_generation or manifest_generation != contract_generation:
            checker.fail("generation_join", "manifest and contract generation_id values must match when supplied", visual_id)
        return manifest_generation or contract_generation
    return ""


def check_route(
    checker: ContractChecker,
    visual: dict[str, Any],
    contract: dict[str, Any],
    visual_id: str,
    claim_ids: set[str],
    source_ids: set[str],
    generation_id: str = "",
) -> None:
    route = string_value(field(contract, "source_visual_route", field(visual, "source_visual_route")), "source_visual_route", checker, visual_id, required=True)
    if route not in ROUTES:
        checker.fail("invalid_route", f"source_visual_route is not one of {sorted(ROUTES)}", visual_id)
        return
    reason = string_value(field(contract, "decision_reason_code", field(visual, "decision_reason_code")), "decision_reason_code", checker, visual_id)
    cutout_ids = string_list(field(contract, "source_cutout_asset_ids", field(visual, "source_cutout_asset_ids")), "source_cutout_asset_ids", checker, visual_id, allow_comma=True)
    cutout_paths = string_list(field(contract, "source_cutout_manifest_paths", field(visual, "source_cutout_manifest_paths")), "source_cutout_manifest_paths", checker, visual_id)
    scan_paths = string_list(field(contract, "source_scan_record_paths", field(visual, "source_scan_record_paths")), "source_scan_record_paths", checker, visual_id)
    if len(cutout_ids) != len(cutout_paths):
        checker.fail("source_cutout_join", "source-cutout IDs and manifest paths must have equal counts", visual_id)
    review_status = check_review_status(
        status_from_contract(contract, "visual_review_status") or field(visual, "visual_review_status"),
        "visual_review_status",
        checker,
        visual_id,
    )
    fidelity = contract.get("fidelity")
    fidelity_status_value = status_from_contract(contract, "fidelity_status") or field(visual, "fidelity_status")
    if fidelity_status_value is None and isinstance(fidelity, dict):
        fidelity_status_value = fidelity.get("status", fidelity.get("fidelity_status"))
    fidelity_status = check_review_status(fidelity_status_value, "fidelity_status", checker, visual_id)
    semantic_status = check_review_status(
        status_from_contract(contract, "semantic_status") or field(visual, "semantic_status"),
        "semantic_status",
        checker,
        visual_id,
    )
    if not semantic_status:
        checker.fail("semantic_status_missing", "claim-bearing visual requires semantic_status", visual_id)
    if checker.strict and semantic_status != "passed":
        checker.fail("semantic_review_pending", "claim-bearing visual requires semantic_status=passed in strict mode", visual_id)
    if route == "not_applicable":
        if scan_paths:
            checker.fail("unexpected_scan_record", "not_applicable route must not declare source_scan_record_paths", visual_id)
        if claim_ids:
            checker.fail("claim_route_missing", "claim-bearing visual cannot use source_visual_route=not_applicable", visual_id)
        return
    if route == "source_figure":
        contract_kind = string_value(
            contract.get("kind", contract.get("visual_kind")),
            "contract.kind",
            checker,
            visual_id,
            required=True,
        )
        if contract_kind != "source_figure":
            checker.fail(
                "source_route_kind_mismatch",
                "source_visual_route=source_figure requires kind=source_figure",
                visual_id,
            )
        if scan_paths:
            checker.fail("source_figure_scan_forbidden", "source_figure route must not use source_scan_record_paths; retain candidate evidence in the figure ledger", visual_id)
        string_value(contract.get("locator", contract.get("source_figure_locator")), "source figure locator", checker, visual_id, required=True)
        if not source_ids:
            checker.fail("source_figure_source_ids_missing", "source_figure route requires source_ids", visual_id)
        if not claim_ids:
            checker.fail("source_figure_claim_ids_missing", "source_figure route requires claim_ids", visual_id)
        figure_id = string_value(field(contract, "figure_id", field(visual, "figure_id")), "source figure figure_id", checker, visual_id, required=True)
        rights_basis = string_value(field(contract, "rights_basis", field(visual, "rights_basis")), "source figure rights_basis", checker, visual_id, required=True)
        if checker.strict and rights_basis.casefold() in UNESTABLISHED_RIGHTS_BASIS:
            checker.fail("rights_basis_unestablished", "source_figure rights_basis must identify an established reuse basis in strict mode", visual_id)
        if not cutout_ids or not cutout_paths:
            checker.fail("source_cutout_missing", "source_figure route requires a source cutout", visual_id)
        source_cutout_time = valid_timestamp(field(contract, "source_cutout_created_at", field(visual, "source_cutout_created_at")))
        if source_cutout_time is None:
            checker.fail("source_cutout_timestamp_missing", "source_figure route requires source_cutout_created_at", visual_id)
        if checker.strict and fidelity_status in {"", "pending", "blocked"}:
            checker.fail("source_fidelity_pending", "source_figure fidelity must be passed or not_required in strict mode", visual_id)
        for asset_id, path in zip(cutout_ids, cutout_paths):
            check_source_cutout(
                checker,
                path,
                asset_id,
                visual_id,
                claim_ids,
                source_ids,
                figure_id,
                fidelity_status,
                rights_basis,
                generation_id,
            )
        return
    if route in RECONSTRUCTION_ROUTES:
        derived_id = string_value(field(contract, "derived_asset_id", field(visual, "derived_asset_id")), "derived_asset_id", checker, visual_id, required=True)
        derived_path = field(contract, "derived_asset_path", field(visual, "derived_asset_path"))
        resolve_record_path(checker, derived_path, "derived_asset_path", visual_id)
        packet_path = field(contract, "visual_comparison_packet_path", field(visual, "visual_comparison_packet_path"))
        string_value(field(contract, "attribution_note", field(visual, "attribution_note")), "attribution_note", checker, visual_id, required=True)
        reason = string_value(reason, "decision_reason_code", checker, visual_id, required=True)
        if reason not in REASONS:
            checker.fail("invalid_decision_reason", f"reconstruction reason must be one of {sorted(REASONS)}", visual_id)
        reconstruction_time = valid_timestamp(field(contract, "reconstruction_created_at", field(visual, "reconstruction_created_at")))
        if reconstruction_time is None:
            checker.fail("reconstruction_timestamp_missing", "reconstruction route requires reconstruction_created_at", visual_id)
        if route == "new_explanatory_visual" and reason == "no_source_figure":
            checker.fail("new_visual_no_source_exception", "new_explanatory_visual cannot use no_source_figure; use no_useful_candidate route", visual_id)
        if reason == "no_source_figure":
            if route != "faithful_reconstruction":
                checker.fail("no_source_exception_route", "only faithful_reconstruction may use no_source_figure", visual_id)
            if cutout_ids or cutout_paths:
                checker.fail("no_source_cutout_present", "no_source_figure exception must not declare a source cutout", visual_id)
            if source_ids:
                checker.fail("no_source_source_ids_present", "faithful no-source reconstruction must keep source_ids empty and use the scan record as the source-search evidence", visual_id)
            if field(contract, "figure_id", field(visual, "figure_id")) not in (None, ""):
                checker.fail("no_source_figure_id_present", "faithful no-source reconstruction must not declare a selected figure_id", visual_id)
            if field(contract, "rights_basis", field(visual, "rights_basis")) not in (None, ""):
                checker.fail("no_source_rights_present", "faithful no-source reconstruction must not declare source rights for a nonexistent figure", visual_id)
            if field(contract, "source_cutout_created_at", field(visual, "source_cutout_created_at")) not in (None, ""):
                checker.fail("no_source_cutout_timestamp_present", "faithful no-source reconstruction must not invent source_cutout_created_at", visual_id)
            if not scan_paths:
                checker.fail("no_source_scan_missing", "faithful no-source reconstruction requires a scan record", visual_id)
            scan_times: list[datetime] = []
            for scan_path in scan_paths:
                _, scan_time = check_structured_record(
                    checker,
                    scan_path,
                    "source-scan record",
                    "no_useful_candidate",
                    visual_id,
                    source_ids,
                    generation_id,
                )
                if scan_time:
                    scan_times.append(scan_time)
            if reconstruction_time:
                for scan_time in scan_times:
                    if reconstruction_time < scan_time:
                        checker.fail("reconstruction_before_scan", "reconstruction_created_at precedes source-scan observation", visual_id)
        else:
            if scan_paths:
                checker.fail("source_backed_scan_unexpected", "source-backed reconstruction must use its source cutout, not a generic scan record", visual_id)
            figure_id = string_value(field(contract, "figure_id", field(visual, "figure_id")), "reconstruction figure_id", checker, visual_id, required=True)
            rights_basis = string_value(field(contract, "rights_basis", field(visual, "rights_basis")), "reconstruction rights_basis", checker, visual_id, required=True)
            if checker.strict and rights_basis.casefold() in UNESTABLISHED_RIGHTS_BASIS:
                checker.fail("rights_basis_unestablished", "source-backed reconstruction rights_basis must identify an established reuse basis in strict mode", visual_id)
            if not source_ids:
                checker.fail("reconstruction_source_ids_missing", "source-backed reconstruction requires source_ids", visual_id)
            if not cutout_ids or not cutout_paths:
                checker.fail("reconstruction_cutout_missing", "source-backed reconstruction requires source cutout IDs and paths", visual_id)
            source_time = valid_timestamp(field(contract, "source_cutout_created_at", field(visual, "source_cutout_created_at")))
            if source_time is None:
                checker.fail("source_cutout_timestamp_missing", "source-backed reconstruction requires source_cutout_created_at", visual_id)
            if source_time and reconstruction_time and reconstruction_time < source_time:
                checker.fail("reconstruction_before_cutout", "reconstruction_created_at precedes source-cutout creation", visual_id)
            for asset_id, path in zip(cutout_ids, cutout_paths):
                check_source_cutout(
                    checker,
                    path,
                    asset_id,
                    visual_id,
                    claim_ids,
                    source_ids,
                    figure_id,
                    fidelity_status,
                    rights_basis,
                    generation_id,
                )
        if not packet_path:
            checker.fail("comparison_packet_missing", "reconstruction route requires a comparison packet", visual_id)
        if checker.strict and review_status != "passed":
            checker.fail("reconstruction_review_pending", "reconstruction route requires visual_review_status=passed in strict mode", visual_id)
        if checker.strict:
            allowed_fidelity = {"passed", "not_required"} if reason == "no_source_figure" else {"passed"}
            if fidelity_status not in allowed_fidelity:
                checker.fail(
                    "reconstruction_fidelity_pending",
                    "source-backed reconstruction fidelity must be passed; only the faithful no-source exception may use not_required",
                    visual_id,
                )
        check_packet(checker, packet_path, visual_id, set(cutout_ids), derived_id, claim_ids, reason, review_status, generation_id)
        return
    if route == "no_useful_candidate":
        if reason != "no_source_figure":
            checker.fail("no_candidate_reason", "no_useful_candidate requires decision_reason_code=no_source_figure", visual_id)
        if cutout_ids or cutout_paths:
            checker.fail("no_candidate_cutout_present", "no_useful_candidate must not declare source-cutout paths", visual_id)
        if not scan_paths:
            checker.fail("no_candidate_scan_missing", "no_useful_candidate requires a scan record", visual_id)
        for scan_path in scan_paths:
            check_structured_record(
                checker,
                scan_path,
                "source-scan record",
                "no_useful_candidate",
                visual_id,
                source_ids,
                generation_id,
            )
        return
    if route == "inaccessible_source":
        if not source_ids:
            checker.fail("inaccessible_source_ids_missing", "inaccessible_source route requires source_ids", visual_id)
        if not scan_paths:
            checker.fail("access_record_missing", "inaccessible_source requires an access record", visual_id)
        for scan_path in scan_paths:
            check_structured_record(
                checker,
                scan_path,
                "source access record",
                "inaccessible_source",
                visual_id,
                source_ids,
                generation_id,
            )
        if checker.strict:
            checker.fail("inaccessible_unresolved", "inaccessible_source is unresolved and cannot pass strict release", visual_id)


def ledger_records(payload: Any, key: str, checker: ContractChecker) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        value = payload.get(key)
        if value is None:
            # Permit a flat list envelope only for the caller that can infer
            # the record type from its key.
            return []
        if not isinstance(value, list):
            checker.fail("invalid_ledger_collection", f"ledger.{key} must be a list")
            return []
        result: list[dict[str, Any]] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                checker.fail("invalid_ledger_record", f"ledger.{key}[{index}] must be an object")
                continue
            result.append(item)
        return result
    if isinstance(payload, list):
        result = []
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                checker.fail("invalid_ledger_record", f"ledger[{index}] must be an object")
                continue
            if key in item:
                result.append(item)
        return result
    return []


def id_set(records: list[dict[str, Any]], key: str, label: str, checker: ContractChecker) -> set[str]:
    result: set[str] = set()
    for index, record in enumerate(records):
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            checker.fail("invalid_ledger_id", f"{label}[{index}].{key} must be a non-empty string")
            continue
        value = value.strip()
        if value in result:
            checker.fail("duplicate_ledger_id", f"{label} contains duplicate {key}={value}")
        result.add(value)
    return result


def collect_contract_records(payload: Any, checker: ContractChecker, label: str) -> list[dict[str, Any]]:
    return records_from_payload(payload, ("contracts", "visuals", "items"), label, checker)


def run(args: argparse.Namespace) -> dict[str, Any]:
    audit_root = args.audit_root.resolve() if args.audit_root else None
    manifest_input = Path(args.manifest).resolve() if args.manifest else None
    base_dir = manifest_input.parent if manifest_input else (audit_root or Path.cwd())
    checker = ContractChecker(strict=args.strict, audit_root=audit_root, base_dir=base_dir)
    if args.strict and audit_root is None:
        checker.warn("audit_root_missing", "strict mode has no audit-root; local referenced paths can only be checked relative to input files")

    manifest_path = checker.local_path(str(args.manifest) if args.manifest else None, "manifest", base=base_dir, visual_id=None)
    manifest_payload = checker.load_payload(manifest_path, "manifest")
    manifest_pages = records_from_payload(manifest_payload, ("slides", "rows", "visuals", "manifest", "items"), "manifest", checker)
    manifest_records, manifest_errors = expand_manifest_visuals(manifest_pages)
    for message in manifest_errors:
        checker.fail("manifest_visuals", message)
    if args.strict and args.manifest and not args.plot:
        checker.fail("storyline_plot_missing", "strict evidence preflight requires --plot/--storyline-plot")
    plot_path = checker.local_path(
        str(args.plot) if args.plot else None,
        "storyline plot",
        base=base_dir,
        required=bool(args.plot),
        visual_id=None,
        require_audit_root=bool(args.plot),
    )
    if plot_path is not None:
        plot_payload = checker.load_payload(plot_path, "storyline plot")
        plot_errors, plot_warnings, plot_metrics = check_plot_payload(
            plot_payload,
            manifest_pages,
            strict=args.strict,
        )
        for message in plot_errors:
            checker.fail("storyline_plot", message)
        for message in plot_warnings:
            checker.warn("storyline_plot", message)
        checker.metrics["storyline_plot"] = plot_metrics
    ledger_path = checker.local_path(str(args.ledger) if args.ledger else None, "ledger", base=base_dir, visual_id=None)
    ledger_payload = checker.load_payload(ledger_path, "ledger")
    if ledger_payload is None:
        checker.fail("ledger_missing", "ledger is required")
    elif isinstance(ledger_payload, dict):
        if not any(key in ledger_payload for key in ("claims", "sources", "assets")):
            checker.fail("ledger_shape", "ledger must declare claims, sources, or assets collections")
    else:
        checker.fail("ledger_shape", "ledger must be a JSON object with claims, sources, and assets collections")
    contract_path = checker.local_path(
        str(args.contract) if args.contract else None,
        "contract",
        base=base_dir,
        required=False,
        visual_id=None,
        require_audit_root=bool(args.contract),
    )
    global_contract_payload = checker.load_payload(contract_path, "contract") if contract_path else None
    global_contract_records = collect_contract_records(global_contract_payload, checker, "contract") if global_contract_payload is not None else []

    claims = ledger_records(ledger_payload, "claims", checker)
    sources = ledger_records(ledger_payload, "sources", checker)
    assets = ledger_records(ledger_payload, "assets", checker)
    claim_ids = id_set(claims, "claim_id", "ledger.claims", checker)
    source_ids = id_set(sources, "source_id", "ledger.sources", checker)
    asset_ids = id_set(assets, "asset_id", "ledger.assets", checker)
    if ledger_payload is not None and isinstance(ledger_payload, dict) and "claims" not in ledger_payload:
        checker.fail("ledger_claims_missing", "ledger.claims collection is required for claim-bearing joins")
    if ledger_payload is not None and isinstance(ledger_payload, dict) and "sources" not in ledger_payload:
        checker.fail("ledger_sources_missing", "ledger.sources collection is required, even when it is empty")

    seen_visuals: set[str] = set()
    contract_cache: dict[Path, list[dict[str, Any]]] = {}
    checked_count = 0
    skipped_count = 0
    for index, visual in enumerate(manifest_records):
        visual_id = string_value(field(visual, "visual_id"), f"manifest[{index}].visual_id", checker, None, required=True)
        if visual_id in seen_visuals:
            checker.fail("duplicate_visual_id", f"manifest contains duplicate visual_id={visual_id}", visual_id)
        if visual_id:
            seen_visuals.add(visual_id)
        slide_id = string_value(field(visual, "slide_id"), f"manifest[{index}].slide_id", checker, visual_id or None, required=True)
        _ = slide_id
        kind = string_value(visual.get("kind", visual.get("visual_kind")), f"manifest[{index}].kind", checker, visual_id or None, required=True)
        claims_for_visual = string_list(field(visual, "claim_ids"), f"manifest[{index}].claim_ids", checker, visual_id or None, allow_comma=True)
        sources_for_visual = string_list(field(visual, "source_ids"), f"manifest[{index}].source_ids", checker, visual_id or None, allow_comma=True)
        explicit_claim_bearing = field(visual, "claim_bearing", _MISSING)
        if explicit_claim_bearing is _MISSING or explicit_claim_bearing is None:
            checker.fail("claim_bearing_missing", "every manifest visual must declare claim_bearing explicitly", visual_id or None)
            # A malformed declaration must not become an implicit non-claim
            # escape hatch. Continue through the claim-bearing validator so
            # the report exposes all missing joins rather than silently
            # counting the row as skipped.
            claim_bearing = True
        else:
            parsed_claim_bearing = boolean_value(explicit_claim_bearing, "manifest.claim_bearing", checker, visual_id or None)
            claim_bearing = parsed_claim_bearing if parsed_claim_bearing is not None else True
        if claims_for_visual and claim_bearing is False:
            checker.fail("claim_bearing_claim_join", "manifest claim_ids cannot be attached to claim_bearing=false", visual_id or None)
            claim_bearing = True
        if not claim_bearing:
            declared_contract = field(visual, "contract_path", None)
            if declared_contract not in (None, ""):
                checker.local_path(
                    declared_contract,
                    "non-claim visual contract_path",
                    base=base_dir,
                    required=True,
                    visual_id=visual_id or None,
                    require_audit_root=True,
                )
            skipped_count += 1
            continue
        checked_count += 1
        if not claims_for_visual:
            checker.fail("claim_ids_missing", "claim-bearing visual requires at least one claim_id", visual_id or None)
        if kind not in SUPPORTED_KINDS:
            checker.fail("unsupported_claim_bearing_kind", f"claim-bearing kind is outside bounded validator: {kind}", visual_id or None)
        for claim_id in claims_for_visual:
            if claim_id not in claim_ids:
                checker.fail("manifest_claim_join", f"manifest claim_id is absent from ledger: {claim_id}", visual_id or None)
        for source_id in sources_for_visual:
            if source_id not in source_ids:
                checker.fail("manifest_source_join", f"manifest source_id is absent from ledger: {source_id}", visual_id or None)
        row_contract_raw = field(visual, "contract_path")
        selected_records: list[dict[str, Any]] = []
        if row_contract_raw is not None:
            row_contract_path = checker.local_path(
                row_contract_raw,
                "manifest contract_path",
                base=base_dir,
                visual_id=visual_id or None,
                require_audit_root=True,
            )
            if row_contract_path:
                if row_contract_path not in contract_cache:
                    contract_cache[row_contract_path] = collect_contract_records(
                        checker.load_payload(row_contract_path, "visual contract", visual_id or None),
                        checker,
                        "visual contract",
                    )
                selected_records = contract_cache[row_contract_path]
        elif global_contract_records:
            selected_records = global_contract_records
        else:
            checker.fail("contract_path_missing", "claim-bearing visual requires contract_path", visual_id or None)
        matches = [record for record in selected_records if field(record, "visual_id") == visual_id]
        if len(matches) == 0:
            checker.fail("contract_visual_join", "no contract record joins to manifest visual_id", visual_id or None)
            continue
        if len(matches) > 1:
            checker.fail("duplicate_contract_visual", "multiple contract records join to manifest visual_id", visual_id or None)
            continue
        contract = matches[0]
        contract_visual_id = string_value(field(contract, "visual_id"), "contract.visual_id", checker, visual_id or None, required=True)
        contract_slide_id = string_value(field(contract, "slide_id"), "contract.slide_id", checker, visual_id or None, required=True)
        contract_kind = string_value(contract.get("kind", contract.get("visual_kind")), "contract.kind", checker, visual_id or None, required=True)
        manifest_reader_role = string_value(field(visual, "reader_role"), "manifest.reader_role", checker, visual_id or None, required=True)
        contract_reader_role = string_value(field(contract, "reader_role"), "contract.reader_role", checker, visual_id or None, required=True)
        manifest_boundary = string_value(visual.get("boundary"), "manifest.boundary", checker, visual_id or None, required=True)
        contract_boundary = string_value(contract.get("boundary"), "contract.boundary", checker, visual_id or None, required=True)
        manifest_status = string_value(visual.get("status"), "manifest.status", checker, visual_id or None, required=True)
        contract_status = string_value(contract.get("status"), "contract.status", checker, visual_id or None, required=True)
        if manifest_reader_role and contract_reader_role and manifest_reader_role != contract_reader_role:
            checker.fail("reader_role_join", "contract.reader_role does not match manifest", visual_id or None)
        if manifest_boundary and contract_boundary and manifest_boundary != contract_boundary:
            checker.fail("boundary_join", "contract.boundary does not match manifest", visual_id or None)
        if manifest_status and contract_status and manifest_status != contract_status:
            checker.fail("content_status_join", "contract.status does not match manifest", visual_id or None)
        manifest_route_raw = field(visual, "source_visual_route")
        manifest_route = string_value(manifest_route_raw, "manifest.source_visual_route", checker, visual_id or None, required=True)
        contract_route = string_value(field(contract, "source_visual_route"), "contract.source_visual_route", checker, visual_id or None, required=True)
        if manifest_route and contract_route and manifest_route != contract_route:
            checker.fail("contract_route_join", "contract.source_visual_route does not match manifest", visual_id or None)
        contract_claim_bearing_raw = field(contract, "claim_bearing", _MISSING)
        contract_claim_bearing = (
            boolean_value(contract_claim_bearing_raw, "contract.claim_bearing", checker, visual_id or None)
            if contract_claim_bearing_raw is not _MISSING and contract_claim_bearing_raw is not None
            else None
        )
        if contract_claim_bearing is None:
            checker.fail("invalid_contract_claim_bearing", "contract.claim_bearing must be boolean", visual_id or None)
        elif contract_claim_bearing is not claim_bearing:
            checker.fail("contract_claim_bearing_join", "contract.claim_bearing does not match manifest", visual_id or None)
        if contract_visual_id != visual_id:
            checker.fail("contract_visual_join", "contract.visual_id does not match manifest", visual_id or None)
        if contract_slide_id != slide_id:
            checker.fail("contract_slide_join", "contract.slide_id does not match manifest", visual_id or None)
        if contract_kind != kind:
            checker.fail("contract_kind_join", "contract.kind does not match manifest", visual_id or None)
        check_contract_review(checker, visual, contract, visual_id)
        contract_claims = set(string_list(field(contract, "claim_ids"), "contract.claim_ids", checker, visual_id or None, required=True, allow_comma=True))
        contract_sources = set(string_list(field(contract, "source_ids"), "contract.source_ids", checker, visual_id or None, allow_comma=True))
        if contract_claims != set(claims_for_visual):
            checker.fail("contract_claim_join", "contract.claim_ids do not match manifest claim_ids", visual_id or None)
        if contract_sources != set(sources_for_visual):
            checker.fail("contract_source_join", "contract.source_ids do not match manifest source_ids", visual_id or None)
        manifest_semantic_status = check_review_status(
            field(visual, "semantic_status"), "manifest.semantic_status", checker, visual_id or None
        )
        contract_semantic_status = check_review_status(
            status_from_contract(contract, "semantic_status"), "contract.semantic_status", checker, visual_id or None
        )
        if not manifest_semantic_status:
            checker.fail("manifest_semantic_status_missing", "claim-bearing manifest row requires semantic_status", visual_id or None)
        if not contract_semantic_status:
            checker.fail("contract_semantic_status_missing", "claim-bearing contract requires semantic_status", visual_id or None)
        if manifest_semantic_status and contract_semantic_status and manifest_semantic_status != contract_semantic_status:
            checker.fail("semantic_status_join", "contract.semantic_status does not match manifest", visual_id or None)
        for status_name in ("visual_review_status", "fidelity_status"):
            manifest_value = field(visual, status_name)
            contract_value = status_from_contract(contract, status_name)
            if manifest_value is not None:
                manifest_status = check_review_status(manifest_value, f"manifest.{status_name}", checker, visual_id or None)
                contract_status = check_review_status(contract_value, f"contract.{status_name}", checker, visual_id or None)
                if manifest_status and contract_status and manifest_status != contract_status:
                    checker.fail(f"{status_name}_join", f"contract.{status_name} does not match manifest", visual_id or None)
        for asset_id in visual_asset_ids(contract):
            if not assets:
                checker.fail("asset_ledger_missing", f"contract references asset {asset_id} but ledger.assets is empty/missing", visual_id or None)
            elif asset_id not in asset_ids:
                checker.fail("contract_asset_join", f"contract asset_id is absent from ledger: {asset_id}", visual_id or None)
        semantics = contract_semantics(contract)
        if not semantics:
            checker.fail("semantics_missing", "claim-bearing contract requires a semantics object", visual_id or None)
        elif kind == "table":
            check_table(semantics, checker, visual_id)
        elif kind == "diagram":
            check_diagram(semantics, checker, visual_id)
        elif kind == "chart":
            check_chart(semantics, checker, visual_id)
        elif kind == "source_figure":
            # Source-figure semantics are checked by the route gate below.
            string_value(contract.get("locator", contract.get("source_figure_locator")), "source figure locator", checker, visual_id, required=True)
        generation_id = check_route_manifest_contract_join(
            checker,
            visual,
            contract,
            visual_id,
            manifest_route,
            string_value(
                field(contract, "decision_reason_code", field(visual, "decision_reason_code")),
                "decision_reason_code",
                checker,
                visual_id,
            ),
        )
        check_route(
            checker,
            visual,
            contract,
            visual_id,
            set(claims_for_visual),
            set(sources_for_visual),
            generation_id,
        )

    # Optional visual ledger is still a join when supplied.
    if isinstance(ledger_payload, dict) and "visuals" in ledger_payload:
        visual_ledger = ledger_records(ledger_payload, "visuals", checker)
        visual_ledger_ids = id_set(visual_ledger, "visual_id", "ledger.visuals", checker)
        if visual_ledger_ids != seen_visuals:
            checker.fail("visual_ledger_join", "ledger.visuals IDs do not match manifest visual IDs")
    checker.metrics.update({
        "manifest_pages": len(manifest_pages),
        "manifest_visuals": len(manifest_records),
        "claim_bearing_visuals": checked_count,
        "non_claim_bearing_visuals_skipped": skipped_count,
        "contracts_loaded": sum(len(records) for records in contract_cache.values()) + len(global_contract_records),
        "ledger_claims": len(claim_ids),
        "ledger_sources": len(source_ids),
        "ledger_assets": len(asset_ids),
    })
    return {
        "status": "fail" if checker.failures else "pass",
        "failures": checker.failures,
        "warnings": checker.warnings,
        "metrics": checker.metrics,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--ledger", "--evidence-ledger", "--asset-ledger", dest="ledger", type=Path)
    parser.add_argument("--contract", "--contract-path", dest="contract", type=Path)
    parser.add_argument("--plot", "--storyline-plot", dest="plot", type=Path)
    parser.add_argument("--audit-root", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = run(args)
    except Exception as exc:  # Never turn malformed audit input into a traceback.
        report = {
            "status": "fail",
            "failures": [{"code": "internal_checker_error", "message": f"checker recovered from {type(exc).__name__}: {exc}"}],
            "warnings": [],
            "metrics": {},
        }
    payload = json.dumps(report, ensure_ascii=False, indent=2, default=str)
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload + "\n", encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            # Preserve the JSON contract on output failures too.
            report.setdefault("failures", []).append({"code": "output_error", "message": str(exc)})
            report["status"] = "fail"
            payload = json.dumps(report, ensure_ascii=False, indent=2, default=str)
    print(payload)
    return 2 if args.strict and report.get("failures") else 0


if __name__ == "__main__":
    sys.exit(main())
