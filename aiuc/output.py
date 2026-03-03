"""Output generation: Excel (4-sheet workbook) + JSON mapping file."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from aiuc.models import ConfidenceTier, MappingOutput

logger = logging.getLogger(__name__)

# ── Style constants ──────────────────────────────────────────────────────────

HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
DIRECT_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
RELATED_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


def _style_header(ws: Worksheet, num_cols: int) -> None:
    """Apply header styling to the first row."""
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", wrap_text=True)
        cell.border = THIN_BORDER


def _auto_width(ws: Worksheet, num_cols: int, max_rows: int) -> None:
    """Auto-fit column widths."""
    for col in range(1, num_cols + 1):
        max_len = 0
        for row in range(1, min(max_rows + 1, 100)):
            val = ws.cell(row=row, column=col).value
            if val:
                max_len = max(max_len, len(str(val)))
        adjusted = min(max_len + 2, 50)
        ws.column_dimensions[get_column_letter(col)].width = adjusted


def _apply_confidence_fill(ws: Worksheet, col: int, start_row: int, end_row: int) -> None:
    """Color-code confidence tier cells."""
    for row in range(start_row, end_row + 1):
        cell = ws.cell(row=row, column=col)
        val = str(cell.value) if cell.value else ""
        if val == ConfidenceTier.DIRECT.value:
            cell.fill = DIRECT_FILL
        elif val == ConfidenceTier.RELATED.value:
            cell.fill = RELATED_FILL
        cell.border = THIN_BORDER


# ── Sheet 1: AIUC → OWASP (Control) ─────────────────────────────────────────


def _write_aiuc_to_owasp_control(wb: Workbook, mapping: MappingOutput) -> None:
    """Write Sheet 1: AIUC → OWASP at control level."""
    ws = wb.create_sheet("AIUC→OWASP (Control)")

    headers = [
        "AIUC ID", "AIUC Title", "AIUC Domain",
        "OWASP ID", "OWASP Title", "Score", "Confidence",
        "Ref Bridge", "Semantic", "Keyword", "Relationship",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    _style_header(ws, len(headers))

    row = 2
    for ctrl in mapping.control_level.aiuc_to_owasp:
        if not ctrl.mappings:
            ws.cell(row=row, column=1, value=ctrl.aiuc_id)
            ws.cell(row=row, column=2, value=ctrl.aiuc_title)
            ws.cell(row=row, column=3, value=ctrl.aiuc_domain)
            ws.cell(row=row, column=4, value="—")
            ws.cell(row=row, column=7, value="None")
            row += 1
            continue

        for m in ctrl.mappings:
            ws.cell(row=row, column=1, value=ctrl.aiuc_id)
            ws.cell(row=row, column=2, value=ctrl.aiuc_title)
            ws.cell(row=row, column=3, value=ctrl.aiuc_domain)
            ws.cell(row=row, column=4, value=m.owasp_id)
            ws.cell(row=row, column=5, value=m.owasp_title)
            ws.cell(row=row, column=6, value=m.score)
            ws.cell(row=row, column=7, value=m.confidence.value)
            ws.cell(row=row, column=8, value=m.signals.reference_bridge)
            ws.cell(row=row, column=9, value=m.signals.semantic)
            ws.cell(row=row, column=10, value=m.signals.keyword)
            ws.cell(row=row, column=11, value=m.relationship_type.value)
            row += 1

    _apply_confidence_fill(ws, 7, 2, row - 1)
    _auto_width(ws, len(headers), row - 1)


# ── Sheet 2: OWASP → AIUC (Control) ─────────────────────────────────────────


def _write_owasp_to_aiuc_control(wb: Workbook, mapping: MappingOutput) -> None:
    """Write Sheet 2: OWASP → AIUC at control level."""
    ws = wb.create_sheet("OWASP→AIUC (Control)")

    headers = [
        "OWASP ID", "OWASP Title", "Rank",
        "AIUC ID", "AIUC Title", "AIUC Domain", "Score", "Confidence",
        "Ref Bridge", "Semantic", "Keyword", "Relationship",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    _style_header(ws, len(headers))

    row = 2
    for entry in mapping.control_level.owasp_to_aiuc:
        if not entry.mappings:
            ws.cell(row=row, column=1, value=entry.owasp_id)
            ws.cell(row=row, column=2, value=entry.owasp_title)
            ws.cell(row=row, column=3, value=entry.owasp_rank)
            ws.cell(row=row, column=4, value="—")
            ws.cell(row=row, column=8, value="None")
            row += 1
            continue

        for m in entry.mappings:
            ws.cell(row=row, column=1, value=entry.owasp_id)
            ws.cell(row=row, column=2, value=entry.owasp_title)
            ws.cell(row=row, column=3, value=entry.owasp_rank)
            ws.cell(row=row, column=4, value=m.aiuc_id)
            ws.cell(row=row, column=5, value=m.aiuc_title)
            ws.cell(row=row, column=6, value=m.aiuc_domain)
            ws.cell(row=row, column=7, value=m.score)
            ws.cell(row=row, column=8, value=m.confidence.value)
            ws.cell(row=row, column=9, value=m.signals.reference_bridge)
            ws.cell(row=row, column=10, value=m.signals.semantic)
            ws.cell(row=row, column=11, value=m.signals.keyword)
            ws.cell(row=row, column=12, value=m.relationship_type.value)
            row += 1

    _apply_confidence_fill(ws, 8, 2, row - 1)
    _auto_width(ws, len(headers), row - 1)


# ── Sheet 3: AIUC → OWASP (Sub-Activity) ────────────────────────────────────


def _write_aiuc_to_owasp_sub(wb: Workbook, mapping: MappingOutput) -> None:
    """Write Sheet 3: AIUC → OWASP at sub-activity level."""
    ws = wb.create_sheet("AIUC→OWASP (Activity)")

    headers = [
        "Activity ID", "Parent Control", "Description",
        "OWASP ID", "Score", "Confidence",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    _style_header(ws, len(headers))

    row = 2
    for act in mapping.sub_activity_level.aiuc_to_owasp:
        if not act.mappings:
            ws.cell(row=row, column=1, value=act.activity_id)
            ws.cell(row=row, column=2, value=act.parent_control)
            ws.cell(row=row, column=3, value=act.description[:100])
            ws.cell(row=row, column=4, value="—")
            ws.cell(row=row, column=6, value="None")
            row += 1
            continue

        for m in act.mappings:
            ws.cell(row=row, column=1, value=act.activity_id)
            ws.cell(row=row, column=2, value=act.parent_control)
            ws.cell(row=row, column=3, value=act.description[:100])
            ws.cell(row=row, column=4, value=m.owasp_id)
            ws.cell(row=row, column=5, value=m.score)
            ws.cell(row=row, column=6, value=m.confidence.value)
            row += 1

    _apply_confidence_fill(ws, 6, 2, row - 1)
    _auto_width(ws, len(headers), row - 1)


# ── Sheet 4: OWASP → AIUC (Sub-Activity) ────────────────────────────────────


def _write_owasp_to_aiuc_sub(wb: Workbook, mapping: MappingOutput) -> None:
    """Write Sheet 4: OWASP → AIUC at sub-activity level."""
    ws = wb.create_sheet("OWASP→AIUC (Activity)")

    headers = [
        "OWASP ID", "OWASP Title",
        "Activity ID", "Parent Control", "Score", "Confidence",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
    _style_header(ws, len(headers))

    row = 2
    for entry in mapping.sub_activity_level.owasp_to_aiuc:
        if not entry.mappings:
            ws.cell(row=row, column=1, value=entry.owasp_id)
            ws.cell(row=row, column=2, value=entry.owasp_title)
            ws.cell(row=row, column=3, value="—")
            ws.cell(row=row, column=6, value="None")
            row += 1
            continue

        for m in entry.mappings:
            ws.cell(row=row, column=1, value=entry.owasp_id)
            ws.cell(row=row, column=2, value=entry.owasp_title)
            ws.cell(row=row, column=3, value=m.activity_id)
            ws.cell(row=row, column=4, value=m.parent_control)
            ws.cell(row=row, column=5, value=m.score)
            ws.cell(row=row, column=6, value=m.confidence.value)
            row += 1

    _apply_confidence_fill(ws, 6, 2, row - 1)
    _auto_width(ws, len(headers), row - 1)


# ── Public API ───────────────────────────────────────────────────────────────


def write_excel(mapping: MappingOutput, output_path: str | Path) -> Path:
    """Write the 4-sheet Excel workbook."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    _write_aiuc_to_owasp_control(wb, mapping)
    _write_owasp_to_aiuc_control(wb, mapping)
    _write_aiuc_to_owasp_sub(wb, mapping)
    _write_owasp_to_aiuc_sub(wb, mapping)

    wb.save(str(path))
    logger.info("Excel written to %s", path)
    return path


def write_json(mapping: MappingOutput, output_path: str | Path) -> Path:
    """Write the mapping output as JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(mapping.model_dump_json())
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    logger.info("JSON written to %s", path)
    return path


def generate_outputs(
    mapping: MappingOutput,
    output_dir: str | Path = "mapping",
) -> tuple[Path, Path]:
    """Generate both Excel and JSON outputs.

    Returns:
        Tuple of (excel_path, json_path).
    """
    out = Path(output_dir)
    excel_path = write_excel(mapping, out / "aiuc_owasp_mapping.xlsx")
    json_path = write_json(mapping, out / "aiuc_owasp_mapping.json")
    return excel_path, json_path
