"""Test harness for rationale and relevance classification.

Runs against:
- AIUC-1 training set (119 mappings from manual crosswalk)
- NIST AI RMF validation set (66 mappings, expert-derived)

Usage:
    pytest tests/test_classification.py -v
    python tests/test_classification.py  # standalone
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiuc.taxonomy import (
    AIUC_CONTROL_FUNCTIONS,
    AIUC_CONTROL_TITLES,
    AIUC_GENERIC_DETECT,
    AIUC_SPECIFIC_DETECT,
    _AIUC_OVERRIDES,
    classify_relevance,
)

TEST_DATA = Path(__file__).parent / "test_data.json"

# NIST-specific classifications
NIST_CONTROL_FUNCTIONS = {
    "GV.1.1": "GOVERN", "GV.1.3": "GOVERN", "GV.1.6": "GOVERN",
    "GV.3.2": "GATE", "GV.4.1": "GOVERN",
    "MP.2.3": "VALID", "MP.3.4": "GOVERN", "MP.4.1": "GATE",
    "MP.5.1": "GOVERN",
    "MS.1.1": "DETECT", "MS.2.3": "VALID", "MS.2.5": "SCOPE",
    "MS.2.6": "VALID", "MS.2.7": "VALID", "MS.2.11": "VALID",
    "MS.4.1": "DETECT",
    "MG.1.1": "VALID", "MG.2.2": "GOVERN", "MG.3.1": "DETECT",
    "MG.3.2": "DETECT", "MG.4.1": "GATE",
}

NIST_CONTROL_TITLES = {
    "GV.1.1": "legal regulatory requirements AI understood managed documented",
    "GV.1.3": "processes determining possible impacts AI system individuals groups",
    "GV.1.6": "mechanisms inventory AI systems",
    "GV.3.2": "policies procedures define differentiate roles responsibilities human-AI oversight",
    "GV.4.1": "organizational practices enable AI testing identification management risks",
    "MP.2.3": "scientific integrity TEVV considerations experimental design data collection uncertainty",
    "MP.3.4": "processes operator practitioner proficiency AI system performance trustworthiness",
    "MP.4.1": "approaches mapping AI technology human oversight manage risks benefits lifecycle",
    "MP.5.1": "likelihood magnitude identified impact expected use foreseeable misuse assessed",
    "MS.1.1": "approaches metrics measurement AI risks MAP function selected implementation",
    "MS.2.3": "AI system performance assurance criteria measured deployment conditions",
    "MS.2.5": "AI system acquisition training evaluation data distribution domain requirements",
    "MS.2.6": "AI system evaluated trustworthy characteristics validity reliability safety fairness security resilience explainability interpretability privacy accountability",
    "MS.2.7": "AI system security resilience MAP function evaluated documented",
    "MS.2.11": "fairness bias MAP function evaluated results documented",
    "MS.4.1": "measurement approaches identifying AI risks deployment context implemented documented monitored",
    "MG.1.1": "determination AI system achieves intended purpose stated objectives deployment context",
    "MG.2.2": "mechanisms sustain value deployed AI systems manage resources risks decommission",
    "MG.3.1": "post-deployment AI system monitoring plans implemented capturing evaluating input users",
    "MG.3.2": "post-deployment mechanisms identify respond AI system risks errors incidents",
    "MG.4.1": "post-deployment monitoring appeal override mechanisms decommissioning protocols change management",
}

NIST_SPECIFIC_DETECT = {"MS.1.1", "MS.4.1", "MG.3.1"}
NIST_GENERIC_DETECT = {"MG.3.2"}


def _run_dataset(name, mappings, get_func, get_title, specific_detect, generic_detect, overrides=None):
    """Run classification against a dataset and return results."""
    total = 0
    rat_correct = 0
    rel_correct = 0
    errors = []

    for threat_id, controls in sorted(mappings.items()):
        for ctrl_id, expected in sorted(controls.items()):
            total += 1
            func = get_func(ctrl_id)
            title = get_title(ctrl_id)

            # Rationale test
            if func == expected["rat"]:
                rat_correct += 1

            # Relevance test
            predicted = classify_relevance(
                ctrl_id, threat_id, func, title,
                specific_detect, generic_detect, overrides,
            )
            if predicted == expected["rel"]:
                rel_correct += 1
            else:
                errors.append({
                    "threat": threat_id,
                    "control": ctrl_id,
                    "expected": expected["rel"],
                    "predicted": predicted,
                    "func": func,
                })

    return {
        "name": name,
        "total": total,
        "rationale_accuracy": rat_correct / total if total else 0,
        "relevance_accuracy": rel_correct / total if total else 0,
        "errors": errors,
    }


def run_all():
    """Run both training and validation sets."""
    with open(TEST_DATA) as f:
        data = json.load(f)

    # Training set (AIUC-1)
    train = _run_dataset(
        "AIUC-1 Training",
        data["training"]["mappings"],
        lambda c: AIUC_CONTROL_FUNCTIONS.get(c, "GOVERN"),
        lambda c: AIUC_CONTROL_TITLES.get(c, ""),
        AIUC_SPECIFIC_DETECT,
        AIUC_GENERIC_DETECT,
        _AIUC_OVERRIDES,
    )

    # Validation set (NIST AI RMF)
    val = _run_dataset(
        "NIST AI RMF Validation",
        data["validation"]["mappings"],
        lambda c: NIST_CONTROL_FUNCTIONS.get(c, "GOVERN"),
        lambda c: NIST_CONTROL_TITLES.get(c, ""),
        NIST_SPECIFIC_DETECT,
        NIST_GENERIC_DETECT,
    )

    return train, val


# ── Pytest tests ─────────────────────────────────────────────────────────────

def test_aiuc_rationale_accuracy():
    train, _ = run_all()
    assert train["rationale_accuracy"] >= 0.99, (
        f"AIUC rationale accuracy {train['rationale_accuracy']:.1%} < 99%"
    )

def test_aiuc_relevance_accuracy():
    train, _ = run_all()
    assert train["relevance_accuracy"] >= 0.98, (
        f"AIUC relevance accuracy {train['relevance_accuracy']:.1%} < 98%"
    )

def test_nist_rationale_accuracy():
    _, val = run_all()
    assert val["rationale_accuracy"] >= 0.99, (
        f"NIST rationale accuracy {val['rationale_accuracy']:.1%} < 99%"
    )

def test_nist_relevance_accuracy():
    _, val = run_all()
    assert val["relevance_accuracy"] >= 0.80, (
        f"NIST relevance accuracy {val['relevance_accuracy']:.1%} < 80%"
    )

def test_generalization_gap():
    train, val = run_all()
    gap = train["relevance_accuracy"] - val["relevance_accuracy"]
    assert gap <= 0.20, (
        f"Generalization gap {gap:.1%} > 20% (train={train['relevance_accuracy']:.1%}, "
        f"val={val['relevance_accuracy']:.1%})"
    )


# ── Standalone runner ────────────────────────────────────────────────────────

if __name__ == "__main__":
    train, val = run_all()

    for result in [train, val]:
        print(f"\n{'='*60}")
        print(f"  {result['name']}")
        print(f"{'='*60}")
        print(f"  Total: {result['total']}")
        print(f"  Rationale accuracy: {result['rationale_accuracy']:.1%}")
        print(f"  Relevance accuracy: {result['relevance_accuracy']:.1%}")
        if result["errors"]:
            print(f"  Errors ({len(result['errors'])})")
            for e in result["errors"]:
                print(f"    {e['threat']}/{e['control']}: "
                      f"exp={e['expected']}, got={e['predicted']} [{e['func']}]")

    gap = train["relevance_accuracy"] - val["relevance_accuracy"]
    print(f"\nGeneralization gap: {gap:.1%}")
