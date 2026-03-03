"""Mapping orchestrator: combines signals → composite scores → bi-directional mappings.

Produces control-level and sub-activity-level mappings between
AIUC-1 and OWASP Top 10 for Agentic Applications.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np

from aiuc.models import (
    AIUC1Standard,
    AIUCToOWASPControl,
    AIUCToOWASPSubActivity,
    ConfidenceTier,
    Control,
    ControlLevelMappings,
    ControlMapping,
    MappingMetadata,
    MappingOutput,
    MappingThresholds,
    MappingWeights,
    OWASPAgenticTop10,
    OWASPControlMapping,
    OWASPEntry,
    OWASPSubActivityMapping,
    OWASPToAIUCControl,
    OWASPToAIUCSubActivity,
    SignalScores,
    SubActivityLevelMappings,
    SubActivityMapping,
    classify_confidence,
    infer_relationship_type,
)
from aiuc.signals import compute_composite_scores

logger = logging.getLogger(__name__)


# ── Anchor pairs for calibration ─────────────────────────────────────────────

ANCHOR_PAIRS: list[dict[str, str]] = [
    # Strong shared LLM refs: D003(LLM06,08,10) ↔ ASI02(LLM06) = Jaccard 1/3
    {"aiuc": "D003", "owasp": "ASI02", "expected": "Related"},
    # Perfect ref overlap: D004(LLM06) ↔ ASI02(LLM06)
    {"aiuc": "D004", "owasp": "ASI02", "expected": "Direct"},
    # Perfect ref overlap: E006(LLM03) ↔ ASI04(LLM03)
    {"aiuc": "E006", "owasp": "ASI04", "expected": "Direct"},
    # Shared LLM01: B001(LLM01,04,05,08) ↔ ASI01(LLM01)
    {"aiuc": "B001", "owasp": "ASI01", "expected": "Related"},
    # C006(LLM05) ↔ ASI05(LLM01,05) = Jaccard 1/2
    {"aiuc": "C006", "owasp": "ASI05", "expected": "Related"},
    # B005(LLM01,04,10) ↔ ASI01(LLM01) = Jaccard 1/3
    {"aiuc": "B005", "owasp": "ASI01", "expected": "Related"},
    # B002(LLM01,08,10) ↔ ASI06(LLM01,04,08) = Jaccard 2/4
    {"aiuc": "B002", "owasp": "ASI06", "expected": "Related"},
    # D003(LLM06,08,10) ↔ ASI10(LLM01,02,06,09) = Jaccard 1/6
    {"aiuc": "D003", "owasp": "ASI10", "expected": "Related"},
    # A005(LLM02,05,08) ↔ ASI03(LLM01,02,06) = Jaccard 1/5
    {"aiuc": "A005", "owasp": "ASI03", "expected": "Related"},
    # B009(LLM02,05,08,09) ↔ ASI09(LLM01,05,06,09) = Jaccard 2/6
    {"aiuc": "B009", "owasp": "ASI09", "expected": "Related"},
]


def _get_domain_for_control(aiuc: AIUC1Standard, control_id: str) -> str:
    """Find the domain name for a given control ID."""
    for domain in aiuc.domains:
        for ctrl in domain.controls:
            if ctrl.id == control_id:
                return domain.name
    return ""


def _flatten_controls(aiuc: AIUC1Standard) -> list[Control]:
    """Flatten all controls from all domains into a single list."""
    controls: list[Control] = []
    for domain in aiuc.domains:
        controls.extend(domain.controls)
    return controls


def _build_control_domain_map(aiuc: AIUC1Standard) -> dict[str, str]:
    """Build a mapping from control ID → domain name."""
    mapping: dict[str, str] = {}
    for domain in aiuc.domains:
        for ctrl in domain.controls:
            mapping[ctrl.id] = domain.name
    return mapping


def run_mapping(
    aiuc: AIUC1Standard,
    owasp: OWASPAgenticTop10,
    weights: MappingWeights | None = None,
    thresholds: MappingThresholds | None = None,
    model_name: str = "all-MiniLM-L6-v2",
) -> MappingOutput:
    """Run the full mapping pipeline.

    Args:
        aiuc: Parsed AIUC-1 standard.
        owasp: Parsed OWASP Agentic Top 10.
        weights: Signal weights (default: 0.45/0.35/0.20).
        thresholds: Confidence tier thresholds.
        model_name: Sentence transformer model for semantic similarity.

    Returns:
        Complete bi-directional mapping output.
    """
    w = weights or MappingWeights()
    t = thresholds or MappingThresholds()

    controls = _flatten_controls(aiuc)
    entries = owasp.entries
    domain_map = _build_control_domain_map(aiuc)

    logger.info(
        "Computing composite scores for %d controls × %d entries",
        len(controls), len(entries),
    )

    weight_tuple = (w.reference_bridge, w.semantic, w.keyword)
    composite, ref_bridge, semantic, keyword = compute_composite_scores(
        controls, entries, weights=weight_tuple, model_name=model_name,
    )

    # ── Control-level mappings ───────────────────────────────────────────
    aiuc_to_owasp = _build_aiuc_to_owasp_control(
        controls, entries, composite, ref_bridge, semantic, keyword, domain_map, t,
    )
    owasp_to_aiuc = _build_owasp_to_aiuc_control(
        controls, entries, composite, ref_bridge, semantic, keyword, domain_map, t,
    )

    # ── Sub-activity-level mappings ──────────────────────────────────────
    sub_aiuc_to_owasp, sub_owasp_to_aiuc = _build_sub_activity_mappings(
        aiuc, controls, entries, composite, ref_bridge, semantic, keyword, t,
    )

    # ── Anchor pair validation ───────────────────────────────────────────
    _validate_anchors(controls, entries, composite, t)

    return MappingOutput(
        metadata=MappingMetadata(
            weights=w,
            thresholds=t,
        ),
        control_level=ControlLevelMappings(
            aiuc_to_owasp=aiuc_to_owasp,
            owasp_to_aiuc=owasp_to_aiuc,
        ),
        sub_activity_level=SubActivityLevelMappings(
            aiuc_to_owasp=sub_aiuc_to_owasp,
            owasp_to_aiuc=sub_owasp_to_aiuc,
        ),
    )


def _build_aiuc_to_owasp_control(
    controls: list[Control],
    entries: list[OWASPEntry],
    composite: np.ndarray,
    ref_bridge: np.ndarray,
    semantic: np.ndarray,
    keyword: np.ndarray,
    domain_map: dict[str, str],
    thresholds: MappingThresholds,
) -> list[AIUCToOWASPControl]:
    """Build AIUC → OWASP control-level mappings."""
    results: list[AIUCToOWASPControl] = []

    for i, ctrl in enumerate(controls):
        mappings: list[ControlMapping] = []

        for j, entry in enumerate(entries):
            score = float(composite[i, j])
            confidence = classify_confidence(score, thresholds)

            if confidence in (ConfidenceTier.NONE, ConfidenceTier.TANGENTIAL):
                continue

            signals = SignalScores(
                reference_bridge=round(float(ref_bridge[i, j]), 3),
                semantic=round(float(semantic[i, j]), 3),
                keyword=round(float(keyword[i, j]), 3),
            )

            mappings.append(ControlMapping(
                owasp_id=entry.identifier,
                owasp_title=entry.title,
                score=round(score, 3),
                confidence=confidence,
                signals=signals,
                relationship_type=infer_relationship_type(signals, ctrl),
            ))

        mappings.sort(key=lambda m: m.score, reverse=True)

        results.append(AIUCToOWASPControl(
            aiuc_id=ctrl.id,
            aiuc_title=ctrl.title,
            aiuc_domain=domain_map.get(ctrl.id, ""),
            mappings=mappings,
        ))

    return results


def _build_owasp_to_aiuc_control(
    controls: list[Control],
    entries: list[OWASPEntry],
    composite: np.ndarray,
    ref_bridge: np.ndarray,
    semantic: np.ndarray,
    keyword: np.ndarray,
    domain_map: dict[str, str],
    thresholds: MappingThresholds,
) -> list[OWASPToAIUCControl]:
    """Build OWASP → AIUC control-level mappings."""
    results: list[OWASPToAIUCControl] = []

    for j, entry in enumerate(entries):
        mappings: list[OWASPControlMapping] = []

        for i, ctrl in enumerate(controls):
            score = float(composite[i, j])
            confidence = classify_confidence(score, thresholds)

            if confidence in (ConfidenceTier.NONE, ConfidenceTier.TANGENTIAL):
                continue

            signals = SignalScores(
                reference_bridge=round(float(ref_bridge[i, j]), 3),
                semantic=round(float(semantic[i, j]), 3),
                keyword=round(float(keyword[i, j]), 3),
            )

            mappings.append(OWASPControlMapping(
                aiuc_id=ctrl.id,
                aiuc_title=ctrl.title,
                aiuc_domain=domain_map.get(ctrl.id, ""),
                score=round(score, 3),
                confidence=confidence,
                signals=signals,
                relationship_type=infer_relationship_type(signals, ctrl),
            ))

        mappings.sort(key=lambda m: m.score, reverse=True)

        results.append(OWASPToAIUCControl(
            owasp_id=entry.identifier,
            owasp_title=entry.title,
            owasp_rank=entry.rank,
            mappings=mappings,
        ))

    return results


def _build_sub_activity_mappings(
    aiuc: AIUC1Standard,
    controls: list[Control],
    entries: list[OWASPEntry],
    composite: np.ndarray,
    ref_bridge: np.ndarray,
    semantic: np.ndarray,
    keyword: np.ndarray,
    thresholds: MappingThresholds,
) -> tuple[list[AIUCToOWASPSubActivity], list[OWASPToAIUCSubActivity]]:
    """Build sub-activity level mappings.

    Uses parent control scores as a base, with activity-specific adjustments
    based on keyword matching against the activity description.
    """
    aiuc_to_owasp: list[AIUCToOWASPSubActivity] = []

    # Index controls for lookup
    ctrl_idx = {c.id: i for i, c in enumerate(controls)}

    # Collect all activities with their parent info
    all_activities: list[tuple[str, str, str, int]] = []  # (act_id, parent_id, desc, ctrl_index)

    for domain in aiuc.domains:
        for ctrl in domain.controls:
            ci = ctrl_idx.get(ctrl.id)
            if ci is None:
                continue
            for act in ctrl.activities:
                all_activities.append((act.id, ctrl.id, act.description, ci))

    for act_id, parent_id, desc, ci in all_activities:
        mappings: list[SubActivityMapping] = []

        for j, entry in enumerate(entries):
            # Start with parent control score
            base_score = float(composite[ci, j])

            # Apply a small activity-specific modifier based on text overlap
            act_lower = desc.lower()
            entry_lower = (entry.title + " " + entry.description).lower()

            # Simple keyword boost: count shared significant words
            stop = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "is"}
            act_words = set(act_lower.split()) - stop
            entry_words = set(entry_lower.split()) - stop
            overlap = len(act_words & entry_words)
            modifier = min(overlap * 0.02, 0.10)  # Cap at +0.10

            score = min(base_score + modifier, 1.0)
            confidence = classify_confidence(score, thresholds)

            if confidence in (ConfidenceTier.NONE, ConfidenceTier.TANGENTIAL):
                continue

            mappings.append(SubActivityMapping(
                owasp_id=entry.identifier,
                score=round(score, 3),
                confidence=confidence,
            ))

        mappings.sort(key=lambda m: m.score, reverse=True)

        aiuc_to_owasp.append(AIUCToOWASPSubActivity(
            activity_id=act_id,
            parent_control=parent_id,
            description=desc,
            mappings=mappings,
        ))

    # Build reverse mapping (OWASP → AIUC sub-activities)
    owasp_to_aiuc: list[OWASPToAIUCSubActivity] = []
    for entry in entries:
        act_mappings: list[OWASPSubActivityMapping] = []
        for act_entry in aiuc_to_owasp:
            for m in act_entry.mappings:
                if m.owasp_id == entry.identifier:
                    act_mappings.append(OWASPSubActivityMapping(
                        activity_id=act_entry.activity_id,
                        parent_control=act_entry.parent_control,
                        score=m.score,
                        confidence=m.confidence,
                    ))
        act_mappings.sort(key=lambda m: m.score, reverse=True)
        owasp_to_aiuc.append(OWASPToAIUCSubActivity(
            owasp_id=entry.identifier,
            owasp_title=entry.title,
            mappings=act_mappings,
        ))

    return aiuc_to_owasp, owasp_to_aiuc


def _validate_anchors(
    controls: list[Control],
    entries: list[OWASPEntry],
    composite: np.ndarray,
    thresholds: MappingThresholds,
) -> None:
    """Log validation results for anchor pairs."""
    ctrl_idx = {c.id: i for i, c in enumerate(controls)}
    entry_idx = {e.identifier: j for j, e in enumerate(entries)}

    for pair in ANCHOR_PAIRS:
        i = ctrl_idx.get(pair["aiuc"])
        j = entry_idx.get(pair["owasp"])
        if i is None or j is None:
            logger.warning(
                "Anchor pair %s ↔ %s: not found",
                pair["aiuc"], pair["owasp"],
            )
            continue

        score = float(composite[i, j])
        actual = classify_confidence(score, thresholds)
        expected = pair["expected"]
        match = "OK" if actual.value == expected else "MISMATCH"

        logger.info(
            "Anchor %s ↔ %s: score=%.3f actual=%s expected=%s [%s]",
            pair["aiuc"], pair["owasp"], score, actual.value, expected, match,
        )


def load_aiuc(path: str | Path) -> AIUC1Standard:
    """Load AIUC-1 standard from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return AIUC1Standard.model_validate(data)


def load_owasp(path: str | Path) -> OWASPAgenticTop10:
    """Load OWASP Agentic Top 10 from JSON file."""
    with open(path) as f:
        data = json.load(f)
    return OWASPAgenticTop10.model_validate(data)
