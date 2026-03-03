"""Output generation: Excel (5-sheet workbook) + JSON mapping file.

The workbook contains a README instructional sheet followed by 4 data sheets.
"""

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

# README-specific styles
SECTION_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
SECTION_FONT = Font(bold=True, size=13, color="1F4E79")
TITLE_FONT = Font(bold=True, size=16, color="1F4E79")
BODY_FONT = Font(size=11)
BODY_WRAP = Alignment(wrap_text=True, vertical="top")
TABLE_HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
TABLE_HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)


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


# ── README Sheet ─────────────────────────────────────────────────────────────


def _readme_section_header(ws: Worksheet, row: int, title: str) -> int:
    """Write a section header spanning columns A-D and return the next row."""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    cell = ws.cell(row=row, column=1, value=title)
    cell.font = SECTION_FONT
    cell.fill = SECTION_FILL
    cell.alignment = Alignment(vertical="center")
    cell.border = THIN_BORDER
    for col in range(2, 5):
        ws.cell(row=row, column=col).border = THIN_BORDER
    return row + 1


def _readme_body_row(ws: Worksheet, row: int, text: str) -> int:
    """Write a body text row merged across A-D and return the next row."""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = BODY_FONT
    cell.alignment = BODY_WRAP
    return row + 1


def _readme_table_header(ws: Worksheet, row: int, headers: list[str]) -> int:
    """Write a table header row and return the next row."""
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.fill = TABLE_HEADER_FILL
        cell.font = TABLE_HEADER_FONT
        cell.alignment = Alignment(horizontal="center", wrap_text=True)
        cell.border = THIN_BORDER
    return row + 1


def _readme_table_row(ws: Worksheet, row: int, values: list[str]) -> int:
    """Write a table data row and return the next row."""
    for col, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=v)
        cell.font = BODY_FONT
        cell.alignment = BODY_WRAP
        cell.border = THIN_BORDER
    return row + 1


def _write_readme_sheet(wb: Workbook) -> None:
    """Write the README instructional sheet as the first tab.

    Covers: workbook overview (FR-2), tab-by-tab guide (FR-3),
    confidence tiers (FR-4), relationship types (FR-5), scoring
    methodology (FR-6), framework glossaries (FR-7), and quick-start (FR-8).
    """
    ws = wb.create_sheet("README", 0)
    num_cols = 4

    # Column widths for print-friendly layout
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 35
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 40

    row = 1

    # ── Title Block ──────────────────────────────────────────────────────
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_cols)
    cell = ws.cell(row=row, column=1, value="AIUC-1 \u2194 OWASP Agentic Top 10 Mapping Workbook")
    cell.font = TITLE_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center")
    row += 2  # blank line

    # ── FR-2: Workbook Overview ──────────────────────────────────────────
    row = _readme_section_header(ws, row, "Workbook Overview")
    row = _readme_body_row(ws, row, (
        "This workbook provides a bi-directional mapping between two AI governance "
        "frameworks: the AIUC-1 Standard (AI Use Case Controls) and the OWASP Top 10 "
        "for Agentic Applications (2026 edition)."
    ))
    row = _readme_body_row(ws, row, (
        "It is designed for compliance officers, risk managers, governance leads, "
        "auditors, and security program managers who need to understand how controls "
        "in one framework relate to risks in the other."
    ))
    row = _readme_body_row(ws, row, (
        "The workbook contains 5 sheets: this README plus 4 data sheets. "
        "The data sheets show mappings at two levels of detail (control-level and "
        "activity-level) in both directions (AIUC\u2192OWASP and OWASP\u2192AIUC)."
    ))
    row += 1  # spacer

    # ── FR-3: Tab-by-Tab Guide ───────────────────────────────────────────
    row = _readme_section_header(ws, row, "Tab-by-Tab Guide")

    # Sheet 1: AIUC→OWASP (Control)
    row = _readme_body_row(ws, row, (
        "\u25B6 Sheet: AIUC\u2192OWASP (Control)"
    ))
    row = _readme_body_row(ws, row, (
        "Purpose: Shows which OWASP agentic risks each AIUC control addresses. "
        "Start here if you have an AIUC control and want to know which OWASP risks "
        "it covers."
    ))
    row = _readme_body_row(ws, row, (
        "How to read a row: Each row shows one AIUC control matched to one OWASP "
        "entry, with a score indicating how strong the connection is."
    ))
    row = _readme_table_header(ws, row, ["Column", "Definition", "", ""])
    col_defs_s1 = [
        ["AIUC ID", "Unique identifier for the AIUC-1 control (e.g., A001, B003)"],
        ["AIUC Title", "Name of the AIUC control"],
        ["AIUC Domain", "Domain category (e.g., Data & Privacy, Security, Safety)"],
        ["OWASP ID", "Identifier for the matched OWASP entry (e.g., ASI01)"],
        ["OWASP Title", "Name of the matched OWASP agentic risk"],
        ["Score", "Composite similarity score from 0.0 to 1.0 (higher = stronger match)"],
        ["Confidence", "Tier: Direct (strong match) or Related (meaningful match)"],
        ["Ref Bridge", "Reference Bridge sub-score: overlap in shared OWASP LLM Top 10 refs"],
        ["Semantic", "Semantic sub-score: NLP text similarity between descriptions"],
        ["Keyword", "Keyword sub-score: TF-IDF term overlap with synonym expansion"],
        ["Relationship", "How the control relates to the risk (e.g., Prevents, Mitigates)"],
    ]
    for c in col_defs_s1:
        row = _readme_table_row(ws, row, [c[0], c[1], "", ""])
    row += 1

    # Sheet 2: OWASP→AIUC (Control)
    row = _readme_body_row(ws, row, (
        "\u25B6 Sheet: OWASP\u2192AIUC (Control)"
    ))
    row = _readme_body_row(ws, row, (
        "Purpose: Shows which AIUC controls address each OWASP agentic risk. "
        "Start here if you have an OWASP risk and want to find relevant controls."
    ))
    row = _readme_body_row(ws, row, (
        "How to read a row: Each row shows one OWASP entry matched to one AIUC "
        "control, with a score and confidence tier."
    ))
    row = _readme_table_header(ws, row, ["Column", "Definition", "", ""])
    col_defs_s2 = [
        ["OWASP ID", "Identifier for the OWASP entry (e.g., ASI01)"],
        ["OWASP Title", "Name of the OWASP agentic risk"],
        ["Rank", "OWASP ranking (1 = highest priority risk)"],
        ["AIUC ID", "Identifier for the matched AIUC control"],
        ["AIUC Title", "Name of the matched AIUC control"],
        ["AIUC Domain", "Domain category of the matched control"],
        ["Score", "Composite similarity score (0.0\u20131.0)"],
        ["Confidence", "Tier: Direct or Related"],
        ["Ref Bridge", "Reference Bridge sub-score"],
        ["Semantic", "Semantic similarity sub-score"],
        ["Keyword", "Keyword overlap sub-score"],
        ["Relationship", "How the control relates to the risk"],
    ]
    for c in col_defs_s2:
        row = _readme_table_row(ws, row, [c[0], c[1], "", ""])
    row += 1

    # Sheet 3: AIUC→OWASP (Activity)
    row = _readme_body_row(ws, row, (
        "\u25B6 Sheet: AIUC\u2192OWASP (Activity)"
    ))
    row = _readme_body_row(ws, row, (
        "Purpose: Granular activity-level view. Each AIUC control has sub-activities; "
        "this sheet maps those individual activities to OWASP risks. Use this for "
        "detailed gap analysis."
    ))
    row = _readme_body_row(ws, row, (
        "How to read a row: Each row shows one AIUC activity (a specific action within "
        "a control) matched to one OWASP entry."
    ))
    row = _readme_table_header(ws, row, ["Column", "Definition", "", ""])
    col_defs_s3 = [
        ["Activity ID", "Unique identifier for the AIUC sub-activity"],
        ["Parent Control", "The AIUC control this activity belongs to"],
        ["Description", "What this activity involves (truncated to 100 chars)"],
        ["OWASP ID", "Identifier for the matched OWASP entry"],
        ["Score", "Composite similarity score (0.0\u20131.0)"],
        ["Confidence", "Tier: Direct or Related"],
    ]
    for c in col_defs_s3:
        row = _readme_table_row(ws, row, [c[0], c[1], "", ""])
    row += 1

    # Sheet 4: OWASP→AIUC (Activity)
    row = _readme_body_row(ws, row, (
        "\u25B6 Sheet: OWASP\u2192AIUC (Activity)"
    ))
    row = _readme_body_row(ws, row, (
        "Purpose: Reverse activity-level view. Shows which AIUC activities address "
        "each OWASP risk. Use this to see the full set of actions relevant to a "
        "specific risk."
    ))
    row = _readme_body_row(ws, row, (
        "How to read a row: Each row shows one OWASP entry matched to one AIUC "
        "activity, with its parent control and score."
    ))
    row = _readme_table_header(ws, row, ["Column", "Definition", "", ""])
    col_defs_s4 = [
        ["OWASP ID", "Identifier for the OWASP entry"],
        ["OWASP Title", "Name of the OWASP agentic risk"],
        ["Activity ID", "Identifier for the matched AIUC sub-activity"],
        ["Parent Control", "The AIUC control this activity belongs to"],
        ["Score", "Composite similarity score (0.0\u20131.0)"],
        ["Confidence", "Tier: Direct or Related"],
    ]
    for c in col_defs_s4:
        row = _readme_table_row(ws, row, [c[0], c[1], "", ""])
    row += 1

    # ── FR-4: Confidence Tier Explanation ─────────────────────────────────
    row = _readme_section_header(ws, row, "Understanding Confidence Tiers")
    row = _readme_body_row(ws, row, (
        "Every mapping is assigned a confidence tier based on its composite score. "
        "The tiers use color coding in the data sheets:"
    ))
    row = _readme_table_header(ws, row, ["Tier", "Color", "Score Range", "Meaning"])

    # Direct row with green fill
    direct_row = row
    row = _readme_table_row(ws, row, [
        "Direct", "Green", "\u2265 0.55",
        "Strong, well-supported connection. The control and risk share significant "
        "overlap in references, meaning, and terminology.",
    ])
    ws.cell(row=direct_row, column=2).fill = DIRECT_FILL

    # Related row with yellow fill
    related_row = row
    row = _readme_table_row(ws, row, [
        "Related", "Yellow", "\u2265 0.35",
        "Meaningful but less direct connection. The control is relevant to the risk "
        "but may only partially address it.",
    ])
    ws.cell(row=related_row, column=2).fill = RELATED_FILL

    row = _readme_table_row(ws, row, [
        "Tangential", "(not shown)", "\u2265 0.20",
        "Weak connection. Filtered out of the data sheets to reduce noise.",
    ])
    row = _readme_table_row(ws, row, [
        "None", "(not shown)", "< 0.20",
        "No meaningful connection. Filtered out of the data sheets.",
    ])
    row += 1

    # ── FR-5: Relationship Type Glossary ─────────────────────────────────
    row = _readme_section_header(ws, row, "Relationship Types")
    row = _readme_body_row(ws, row, (
        "Each mapping includes a relationship type that describes how the AIUC "
        "control relates to the OWASP risk:"
    ))
    row = _readme_table_header(ws, row, ["Type", "Meaning", "", ""])
    rel_types = [
        ["Prevents", (
            "The control is designed to stop the risk from occurring. "
            "Preventative controls act before an incident happens."
        )],
        ["Detects", (
            "The control is designed to identify when the risk is being exploited. "
            "Detective controls monitor for signs of an active threat."
        )],
        ["Mitigates", (
            "The control reduces the impact or likelihood of the risk. "
            "It may not fully prevent the risk but limits its consequences."
        )],
        ["Addresses", (
            "The control is relevant to the risk and provides meaningful coverage. "
            "Inferred from strong semantic or reference overlap."
        )],
        ["Partially Addresses", (
            "The control has some relevance but does not fully cover the risk. "
            "May require additional controls for complete coverage."
        )],
    ]
    for rt in rel_types:
        row = _readme_table_row(ws, row, [rt[0], rt[1], "", ""])
    row += 1

    # ── FR-6: Score & Methodology ────────────────────────────────────────
    row = _readme_section_header(ws, row, "Scoring Methodology")
    row = _readme_body_row(ws, row, (
        "Each mapping has a composite score from 0.0 to 1.0 that measures how "
        "strongly an AIUC control relates to an OWASP risk. The score combines "
        "three independent signals:"
    ))
    row = _readme_body_row(ws, row, (
        "Composite Score = 0.45 \u00D7 Reference Bridge + 0.35 \u00D7 Semantic "
        "+ 0.20 \u00D7 Keyword"
    ))
    row += 1
    row = _readme_table_header(ws, row, [
        "Signal", "Weight", "Method", "What It Measures",
    ])
    signals = [
        [
            "Reference Bridge", "45%",
            "Jaccard overlap on shared OWASP LLM Top 10 references",
            "If both the AIUC control and OWASP entry cite the same LLM "
            "vulnerabilities (e.g., LLM01, LLM06), they score higher. This is "
            "the strongest signal because shared references indicate the two "
            "frameworks are talking about the same underlying issue.",
        ],
        [
            "Semantic Similarity", "35%",
            "Sentence-transformer NLP embeddings",
            "Measures how similar the descriptions and guidance text are in "
            "meaning, even if they use different words. Uses the all-MiniLM-L6-v2 "
            "model to convert text into numerical vectors and compute cosine "
            "similarity.",
        ],
        [
            "TF-IDF Keyword", "20%",
            "TF-IDF with domain-specific synonym expansion",
            "Catches explicit term matches between the two texts. Includes "
            "synonym expansion so that 'authentication' matches 'access control' "
            "and similar domain-specific equivalences.",
        ],
    ]
    for s in signals:
        row = _readme_table_row(ws, row, s)
    row += 1

    row = _readme_body_row(ws, row, (
        "Score range: 0.0 (no connection) to 1.0 (perfect match). "
        "In practice, scores above 0.55 indicate strong connections and scores "
        "between 0.35 and 0.55 indicate meaningful but weaker connections."
    ))
    row += 1

    # ── FR-7: Framework Quick-Reference Glossaries ───────────────────────
    row = _readme_section_header(ws, row, "AIUC-1 Domains Quick Reference")
    row = _readme_table_header(ws, row, ["Domain", "ID Range", "Focus", ""])
    aiuc_domains = [
        ["A \u2014 Data & Privacy", "A001\u2013A007",
         "Data leakage, PII protection, IP rights"],
        ["B \u2014 Security", "B001\u2013B009",
         "Adversarial robustness, input filtering, access control"],
        ["C \u2014 Safety", "C001\u2013C012",
         "Harmful/out-of-scope outputs, vulnerability prevention"],
        ["D \u2014 Reliability", "D001\u2013D004",
         "Hallucination prevention, unsafe tool call restriction"],
        ["E \u2014 Accountability", "E001\u2013E017",
         "Vendor management, audit logging, regulatory compliance"],
        ["F \u2014 Society", "F001\u2013F002",
         "Societal impact, responsible disclosure"],
    ]
    for d in aiuc_domains:
        row = _readme_table_row(ws, row, [d[0], d[1], d[2], ""])
    row += 1

    row = _readme_section_header(ws, row, "OWASP Agentic Top 10 (2026) Quick Reference")
    row = _readme_table_header(ws, row, ["Rank", "ID", "Title", "Description"])
    owasp_entries = [
        ["1", "ASI01", "Agent Goal Hijack",
         "Attackers manipulate an agent's objectives or decision pathways through "
         "prompt injection, deceptive outputs, or poisoned data."],
        ["2", "ASI02", "Tool Misuse and Exploitation",
         "Agents misuse legitimate tools due to prompt injection, misalignment, "
         "or unsafe delegation, leading to data exfiltration or workflow hijacking."],
        ["3", "ASI03", "Identity & Privilege Abuse",
         "Agents inherit or escalate privileges beyond what is needed, enabling "
         "unauthorized access to systems and data."],
        ["4", "ASI04", "Agentic Supply Chain Vulnerabilities",
         "Compromised tools, plugins, MCP servers, or dependencies introduce "
         "malicious capabilities into the agent's environment."],
        ["5", "ASI05", "Unexpected Code Execution",
         "Agents generate and execute code that performs unintended or malicious "
         "actions, including arbitrary command execution."],
        ["6", "ASI06", "Memory & Context Poisoning",
         "Persistent corruption of an agent's stored context or long-term memory "
         "alters future behavior without direct attacker control."],
        ["7", "ASI07", "Multi-Agent Trust Issues",
         "Agents in multi-agent systems trust peer messages without verification, "
         "enabling impersonation and coordinated manipulation."],
        ["8", "ASI08", "Insufficient Monitoring & Logging",
         "Lack of comprehensive logging and behavioral monitoring makes it "
         "difficult to detect agent misuse or compromise."],
        ["9", "ASI09", "Lack of Human Oversight",
         "Agents operate autonomously without adequate human review or approval "
         "gates for high-impact decisions."],
        ["10", "ASI10", "Rogue Agents",
         "Agents develop autonomous misalignment, pursuing goals that diverge "
         "from intended objectives without active attacker involvement."],
    ]
    for e in owasp_entries:
        row = _readme_table_row(ws, row, e)
    row += 1

    # ── FR-8: How to Get Started ─────────────────────────────────────────
    row = _readme_section_header(ws, row, "How to Get Started")
    steps = [
        "1. You're here! Read this README tab to understand the workbook structure.",
        (
            "2. Choose your starting point: If you have an AIUC control, go to "
            "'AIUC\u2192OWASP (Control)'. If you have an OWASP risk, go to "
            "'OWASP\u2192AIUC (Control)'."
        ),
        (
            "3. Look at Direct (green) mappings first \u2014 these are the strongest, "
            "most well-supported connections."
        ),
        (
            "4. For more granular detail, use the Activity-level tabs to see "
            "which specific sub-activities within a control are relevant."
        ),
        (
            "5. Use the Score and sub-scores (Ref Bridge, Semantic, Keyword) to "
            "understand why a mapping was made and how confident you can be in it."
        ),
    ]
    for step in steps:
        row = _readme_body_row(ws, row, step)

    # Set print area
    ws.print_area = f"A1:D{row}"
    ws.sheet_properties.pageSetUpPr.fitToPage = True


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
    """Write the 5-sheet Excel workbook (README + 4 data sheets)."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    _write_readme_sheet(wb)
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
