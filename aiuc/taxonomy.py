"""Control-function taxonomy and threat profiles for OWASP ASI mapping.

This module provides the classification rules for:
1. Assigning rationale codes (PREV/SCOPE/GATE/DETECT/VALID/GOVERN/ISOLATE/DISCLOSE)
2. Classifying relevance (Primary/Secondary) per (control, threat) pair

Version: 1.0
Date: 2026-04-06
Owner: Rock Lambros, RockCyber LLC
"""

from __future__ import annotations

import re
from typing import Literal

Rationale = Literal["PREV", "SCOPE", "GATE", "DETECT", "VALID", "GOVERN", "ISOLATE", "DISCLOSE"]

RATIONALE_LABELS: dict[str, str] = {
    "PREV": "Prevent",
    "SCOPE": "Constrain scope",
    "GATE": "Human gate",
    "DETECT": "Detect and trace",
    "VALID": "Validate and test",
    "GOVERN": "Policy and governance",
    "ISOLATE": "Isolate and contain",
    "DISCLOSE": "Disclose and calibrate",
}
Relevance = Literal["Primary", "Secondary"]
DetectRule = Literal["all", "generic_only", "specific_only", "never"]

# ── Static control-function classifications ──────────────────────────────────
# Each control is assigned exactly one function class.
# For new standards, classify using FUNCTION_KEYWORDS below.

AIUC_CONTROL_FUNCTIONS: dict[str, Rationale] = {
    "A001": "GOVERN", "A002": "GOVERN", "A003": "SCOPE", "A004": "SCOPE",
    "A005": "ISOLATE", "A006": "ISOLATE", "A007": "SCOPE",
    "B001": "VALID", "B002": "PREV", "B003": "PREV", "B004": "PREV",
    "B005": "PREV", "B006": "SCOPE", "B007": "SCOPE", "B008": "ISOLATE",
    "B009": "SCOPE",
    "C001": "GOVERN", "C002": "VALID", "C003": "PREV", "C004": "PREV",
    "C005": "PREV", "C006": "PREV", "C007": "GATE", "C008": "DETECT",
    "C009": "GATE", "C010": "VALID", "C011": "VALID", "C012": "VALID",
    "D001": "PREV", "D002": "VALID", "D003": "SCOPE", "D004": "VALID",
    "E001": "GOVERN", "E002": "GOVERN", "E003": "GOVERN", "E004": "GOVERN",
    "E005": "GOVERN", "E006": "VALID", "E007": "GOVERN", "E008": "GOVERN",
    "E009": "DETECT", "E010": "GOVERN", "E011": "GOVERN", "E012": "GOVERN",
    "E013": "GOVERN", "E014": "GOVERN", "E015": "DETECT", "E016": "DISCLOSE",
    "E017": "DISCLOSE",
    "F001": "PREV", "F002": "DETECT",
}

# DETECT subcategories: specific monitoring vs generic logging
AIUC_SPECIFIC_DETECT: set[str] = {"E009", "C008"}
AIUC_GENERIC_DETECT: set[str] = {"E015", "F002"}

# AIUC control titles for topic matching
AIUC_CONTROL_TITLES: dict[str, str] = {
    "A001": "establish input data policy", "A002": "establish output data policy",
    "A003": "limit ai agent data collection", "A004": "protect ip trade secrets",
    "A005": "prevent cross-customer data exposure", "A006": "prevent pii leakage",
    "A007": "prevent ip violations",
    "B001": "third-party testing adversarial robustness",
    "B002": "detect adversarial input", "B003": "manage public release technical details",
    "B004": "prevent ai endpoint scraping",
    "B005": "implement real-time input filtering",
    "B006": "prevent unauthorized ai agent actions",
    "B007": "enforce user access privileges ai systems",
    "B008": "protect model deployment environment",
    "B009": "limit output over-exposure",
    "C001": "define ai risk taxonomy", "C002": "conduct pre-deployment testing",
    "C003": "prevent harmful outputs", "C004": "prevent out-of-scope outputs",
    "C005": "prevent customer-defined high risk outputs",
    "C006": "prevent output vulnerabilities",
    "C007": "flag high risk outputs", "C008": "monitor ai risk categories",
    "C009": "enable real-time feedback and intervention",
    "C010": "third-party testing harmful outputs",
    "C011": "third-party testing out-of-scope outputs",
    "C012": "third-party testing customer-defined risk",
    "D001": "prevent hallucinated outputs",
    "D002": "third-party testing hallucinations",
    "D003": "restrict unsafe tool calls",
    "D004": "third-party testing tool calls",
    "E001": "ai failure plan security breaches",
    "E002": "ai failure plan harmful outputs",
    "E003": "ai failure plan hallucinations",
    "E004": "assign accountability",
    "E005": "assess cloud vs on-prem processing",
    "E006": "conduct vendor due diligence",
    "E007": "document system change approvals",
    "E008": "review internal processes",
    "E009": "monitor third-party access",
    "E010": "establish ai acceptable use policy",
    "E015": "log model activity",
    "E016": "implement ai disclosure mechanisms",
    "E017": "document system transparency policy",
    "F001": "prevent ai cyber misuse",
    "F002": "prevent catastrophic misuse",
}

# ── Keyword rules for classifying new standards ──────────────────────────────

FUNCTION_KEYWORDS: dict[Rationale, list[str]] = {
    "PREV":    ["prevent", "block", "filter", "restrict input", "detect adversarial"],
    "SCOPE":   ["limit", "constrain", "minimize", "least privilege", "access control",
                "unauthorized", "restrict", "scope", "data distribution"],
    "GATE":    ["human review", "approval", "intervention", "feedback", "flag",
                "pause", "stop", "override", "human.*oversight", "appeal"],
    "DETECT":  ["log", "monitor", "audit", "trace", "detect", "alert",
                "observe", "measurement", "post-deployment.*monitor"],
    "VALID":   ["test", "assess", "evaluate", "audit", "verify", "red team",
                "penetration", "due diligence", "TEVV", "assurance criteria"],
    "GOVERN":  ["policy", "plan", "accountability", "process", "compliance",
                "acceptable use", "change approval", "quality management",
                "inventory", "regulatory", "decommission", "lifecycle"],
    "ISOLATE": ["isolate", "contain", "sandbox", "segment", "separate",
                "deployment environment", "tenant"],
    "DISCLOSE":["disclose", "transparency", "provenance", "label", "watermark",
                "model card", "interpretability"],
}

# ── Threat profiles for relevance classification ─────────────────────────────
# Each OWASP ASI entry defines:
#   - primary_functions: function classes always Primary for this threat
#   - primary_topics: regex patterns on control title that indicate Primary
#   - detect_rule: how DETECT controls are classified
#   - disclose_primary: specific DISCLOSE controls that are Primary

THREAT_PROFILES: dict[str, dict] = {
    "ASI01": {
        "primary_functions": {"GATE"},
        "primary_topics": ["adversarial", "goal hijack", "input filter",
                          "unauthorized.*action", "unsafe tool call"],
        "detect_rule": "never",
    },
    "ASI02": {
        "primary_functions": set(),
        "primary_topics": ["tool call", "data collection", "access privilege",
                          "unauthorized.*action", "third-party.*access",
                          "security.*resilience", "data distribution",
                          "post-deployment.*monitoring.*plan"],
        "detect_rule": "specific_only",
    },
    "ASI03": {
        "primary_functions": {"ISOLATE"},
        "primary_topics": ["access privilege", "unauthorized.*action",
                          "unsafe tool call", "third-party.*access",
                          "security.*resilience", "data distribution",
                          "post-deployment.*monitoring"],
        "detect_rule": "specific_only",
    },
    "ASI04": {
        "primary_functions": {"ISOLATE"},
        "primary_topics": ["vendor", "due diligence", "scientific integrity",
                          "TEVV"],
        "detect_rule": "specific_only",
    },
    "ASI05": {
        "primary_functions": {"ISOLATE"},
        "primary_topics": ["output vulnerabilit", "unauthorized.*action",
                          "unsafe tool call", "deployment environment",
                          "tool call.*test", "testing.*tool call",
                          "security.*resilience", "TEVV", "scientific integrity"],
        "detect_rule": "never",
    },
    "ASI06": {
        "primary_functions": set(),
        "primary_topics": ["adversarial", "input filter", "data collection",
                          "cross-customer", "data distribution",
                          "security.*resilience", "measurement.*risk"],
        "detect_rule": "specific_only",
    },
    "ASI07": {
        "primary_functions": {"ISOLATE"},
        "primary_topics": ["unauthorized.*action", "deployment environment",
                          "security.*resilience"],
        "detect_rule": "all",
    },
    "ASI08": {
        "primary_functions": set(),
        "primary_topics": ["hallucin", "unsafe tool call",
                          "appeal.*override", "decommission",
                          "post-deployment.*monitoring.*plan",
                          "failure plan", "sustain.*value.*manage.*risk"],
        "detect_rule": "generic_only",
    },
    "ASI09": {
        "primary_functions": set(),
        "primary_topics": ["harmful output", "hallucin", "testing.*harmful",
                          "fairness.*bias", "human.*oversight",
                          "roles.*responsibilities.*human"],
        "detect_rule": "never",
        "disclose_primary": ["E016"],
    },
    "ASI10": {
        "primary_functions": {"ISOLATE"},
        "primary_topics": ["unauthorized.*action", "unsafe tool call",
                          "deployment environment", "tool call.*test",
                          "testing.*tool call", "security.*resilience",
                          "appeal.*override", "decommission",
                          "failure plan"],
        "detect_rule": "generic_only",
    },
}

# Threat function profiles: which function classes are relevant per threat
# Used for the function-match signal in the composite score
THREAT_FUNCTION_PROFILES: dict[str, set[Rationale]] = {
    "ASI01": {"PREV", "SCOPE", "GATE", "VALID", "DETECT", "GOVERN"},
    "ASI02": {"SCOPE", "VALID", "DETECT", "GATE", "ISOLATE"},
    "ASI03": {"SCOPE", "ISOLATE", "DETECT", "VALID", "GOVERN"},
    "ASI04": {"ISOLATE", "VALID", "DETECT", "SCOPE", "GOVERN"},
    "ASI05": {"SCOPE", "ISOLATE", "PREV", "VALID", "DETECT"},
    "ASI06": {"PREV", "SCOPE", "ISOLATE", "VALID", "DETECT"},
    "ASI07": {"SCOPE", "ISOLATE", "DETECT"},
    "ASI08": {"PREV", "SCOPE", "GOVERN", "DETECT", "GATE", "VALID"},
    "ASI09": {"PREV", "GATE", "VALID", "DISCLOSE", "SCOPE", "DETECT"},
    "ASI10": {"SCOPE", "ISOLATE", "VALID", "GOVERN", "DETECT", "GATE",
              "PREV", "DISCLOSE"},
}

# ── AIUC-specific overrides ──────────────────────────────────────────────────
# These handle cases where the general rules need control-specific exceptions

_AIUC_OVERRIDES: dict[tuple[str, str], Relevance] = {
    ("E015", "ASI06"): "Primary",   # Logging is Primary for invisible poisoning
    ("E015", "ASI07"): "Primary",   # Logging is Primary for multi-agent threats
    ("E015", "ASI08"): "Primary",   # Logging is Primary for cascading failures
    ("E015", "ASI10"): "Primary",   # Logging is Primary for rogue agents
    ("A006", "ASI06"): "Secondary", # PII isolation is Secondary for poisoning
    ("E001", "ASI08"): "Primary",   # Failure plans are Primary for cascading failures
    ("E002", "ASI08"): "Primary",
    ("E003", "ASI08"): "Primary",
    ("E001", "ASI10"): "Primary",   # Failure plans are Primary for rogue agents
    ("C007", "ASI09"): "Primary",   # Flagging high-risk outputs is Primary for trust
    ("C009", "ASI09"): "Primary",   # Real-time intervention is Primary for trust
    ("C009", "ASI01"): "Primary",   # Intervention is Primary for hijack
    ("C007", "ASI01"): "Primary",   # Flagging is Primary for hijack (not in GT but defensive)
}


# ── Classification functions ─────────────────────────────────────────────────

def classify_rationale(ctrl_id: str, standard: str = "AIUC") -> Rationale:
    """Return the rationale code for a control."""
    if standard == "AIUC":
        return AIUC_CONTROL_FUNCTIONS.get(ctrl_id, "GOVERN")
    # For other standards, look up or classify via keywords
    raise ValueError(f"Unknown standard: {standard}")


def classify_relevance(
    ctrl_id: str,
    threat_id: str,
    func: Rationale,
    ctrl_title: str,
    specific_detect: set[str],
    generic_detect: set[str],
    overrides: dict[tuple[str, str], Relevance] | None = None,
) -> Relevance:
    """Classify a (control, threat) pair as Primary or Secondary."""
    # Check overrides first
    if overrides and (ctrl_id, threat_id) in overrides:
        return overrides[(ctrl_id, threat_id)]

    profile = THREAT_PROFILES.get(threat_id, {})
    text = ctrl_title.lower()

    # DETECT handling
    if func == "DETECT":
        rule: DetectRule = profile.get("detect_rule", "never")
        if rule == "all":
            return "Primary"
        if rule == "generic_only" and ctrl_id in generic_detect:
            return "Primary"
        if rule == "specific_only" and ctrl_id in specific_detect:
            return "Primary"
        return "Secondary"

    # DISCLOSE handling
    if func == "DISCLOSE":
        if ctrl_id in profile.get("disclose_primary", []):
            return "Primary"
        return "Secondary"

    # Function-class match
    if func in profile.get("primary_functions", set()):
        return "Primary"

    # Topic match
    for pattern in profile.get("primary_topics", []):
        if re.search(pattern, text):
            return "Primary"

    return "Secondary"


def classify_aiuc(
    ctrl_id: str,
    threat_id: str,
) -> tuple[Rationale, Relevance]:
    """Classify an AIUC-1 control against an OWASP ASI threat."""
    func = AIUC_CONTROL_FUNCTIONS.get(ctrl_id, "GOVERN")
    title = AIUC_CONTROL_TITLES.get(ctrl_id, "")
    rel = classify_relevance(
        ctrl_id, threat_id, func, title,
        AIUC_SPECIFIC_DETECT, AIUC_GENERIC_DETECT,
        _AIUC_OVERRIDES,
    )
    return func, rel
