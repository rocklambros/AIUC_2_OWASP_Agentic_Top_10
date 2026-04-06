"""Evaluate pipeline output against manual ground truth.

Computes precision, recall, F1, rationale accuracy, and relevance accuracy
by comparing the v2 JSON output against tests/test_data.json training set.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure project root is importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> None:
    mapping_path = ROOT / "mapping" / "aiuc_owasp_mapping.json"
    schema_path = ROOT / "schemas" / "crosswalk-mapping-v2.schema.json"
    gt_path = ROOT / "tests" / "test_data.json"

    # ── Load and validate output ────────────────────────────────────────
    with open(mapping_path) as f:
        output = json.load(f)

    with open(schema_path) as f:
        schema = json.load(f)

    import jsonschema

    try:
        jsonschema.validate(output, schema)
        print("Schema validation: PASSED\n")
    except jsonschema.ValidationError as e:
        print(f"Schema validation: FAILED - {e.message}")
        print(f"  Path: {list(e.absolute_path)}")
        sys.exit(1)

    # ── Load ground truth ───────────────────────────────────────────────
    with open(gt_path) as f:
        gt_data = json.load(f)

    gt_mappings: dict[str, dict[str, dict[str, str]]] = gt_data["training"]["mappings"]

    # ── Build pipeline lookup: ASI -> {ctrl_id: {rationale_code, relevance}} ─
    pipeline_by_asi: dict[str, dict[str, dict[str, str]]] = {}
    for entry in output["control_level"]["owasp_to_source"]:
        asi_id = entry["owasp_id"]
        ctrls: dict[str, dict[str, str]] = {}
        for m in entry["mappings"]:
            ctrls[m["control_id"]] = {
                "rationale_code": m["rationale_code"],
                "relevance": m["relevance"],
            }
        pipeline_by_asi[asi_id] = ctrls

    # ── Compute per-ASI metrics ─────────────────────────────────────────
    total_tp = 0
    total_fn = 0
    total_fp = 0
    rationale_correct = 0
    relevance_correct = 0
    rationale_total = 0
    relevance_total = 0

    print(f"{'ASI':<8} {'TP':>4} {'FN':>4} {'FP':>4}  "
          f"{'Prec':>6} {'Rec':>6} {'F1':>6}")
    print("-" * 52)

    for asi_id in sorted(gt_mappings.keys()):
        gt_ctrls = set(gt_mappings[asi_id].keys())
        pipe_ctrls = set(pipeline_by_asi.get(asi_id, {}).keys())

        tp_set = gt_ctrls & pipe_ctrls
        fn_set = gt_ctrls - pipe_ctrls
        fp_set = pipe_ctrls - gt_ctrls

        tp = len(tp_set)
        fn = len(fn_set)
        fp = len(fp_set)

        total_tp += tp
        total_fn += fn
        total_fp += fp

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

        print(f"{asi_id:<8} {tp:>4} {fn:>4} {fp:>4}  "
              f"{prec:>6.1%} {rec:>6.1%} {f1:>6.1%}")

        # Classification accuracy for TPs
        for ctrl_id in tp_set:
            gt_entry = gt_mappings[asi_id][ctrl_id]
            pipe_entry = pipeline_by_asi[asi_id][ctrl_id]

            rationale_total += 1
            if pipe_entry["rationale_code"] == gt_entry["rat"]:
                rationale_correct += 1

            relevance_total += 1
            if pipe_entry["relevance"] == gt_entry["rel"]:
                relevance_correct += 1

    # ── Aggregate metrics ───────────────────────────────────────────────
    print("-" * 52)
    agg_prec = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    agg_rec = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    agg_f1 = (
        2 * agg_prec * agg_rec / (agg_prec + agg_rec)
        if (agg_prec + agg_rec) > 0 else 0.0
    )
    print(f"{'TOTAL':<8} {total_tp:>4} {total_fn:>4} {total_fp:>4}  "
          f"{agg_prec:>6.1%} {agg_rec:>6.1%} {agg_f1:>6.1%}")

    rat_acc = rationale_correct / rationale_total if rationale_total > 0 else 0.0
    rel_acc = relevance_correct / relevance_total if relevance_total > 0 else 0.0

    print(f"\n{'='*52}")
    print("Summary")
    print(f"{'='*52}")
    gt_total = sum(len(v) for v in gt_mappings.values())
    pipe_total = sum(len(v) for v in pipeline_by_asi.values())
    print(f"  Ground truth mappings:  {gt_total}")
    print(f"  Pipeline mappings:      {pipe_total}")
    print(f"  True positives:         {total_tp}")
    print(f"  False negatives:        {total_fn}")
    print(f"  False positives:        {total_fp}")
    print(f"  Precision:              {agg_prec:.1%}")
    print(f"  Recall:                 {agg_rec:.1%}")
    print(f"  F1:                     {agg_f1:.1%}")
    print(f"  Rationale accuracy:     {rat_acc:.1%} ({rationale_correct}/{rationale_total})")
    print(f"  Relevance accuracy:     {rel_acc:.1%} ({relevance_correct}/{relevance_total})")

    # ── Diagnostics if targets missed ───────────────────────────────────
    if agg_rec < 0.50 or agg_prec < 0.80:
        print(f"\n{'='*52}")
        print("Diagnostics (targets not met)")
        print(f"{'='*52}")

        if agg_rec < 0.50:
            print("\nMissed mappings (false negatives):")
            for asi_id in sorted(gt_mappings.keys()):
                gt_ctrls = set(gt_mappings[asi_id].keys())
                pipe_ctrls = set(pipeline_by_asi.get(asi_id, {}).keys())
                missed = sorted(gt_ctrls - pipe_ctrls)
                if missed:
                    print(f"  {asi_id}: {', '.join(missed)}")

        if agg_prec < 0.80:
            print("\nExtra mappings (false positives):")
            for asi_id in sorted(gt_mappings.keys()):
                gt_ctrls = set(gt_mappings[asi_id].keys())
                pipe_ctrls = set(pipeline_by_asi.get(asi_id, {}).keys())
                extra = sorted(pipe_ctrls - gt_ctrls)
                if extra:
                    print(f"  {asi_id}: {', '.join(extra)}")

    # ── Target check ────────────────────────────────────────────────────
    print(f"\n{'='*52}")
    print("Target Check")
    print(f"{'='*52}")
    targets = [
        ("Pipeline mappings >= 60", pipe_total >= 60),
        ("Precision >= 0.80", agg_prec >= 0.80),
        ("Recall >= 0.50", agg_rec >= 0.50),
        ("F1 >= 0.60", agg_f1 >= 0.60),
    ]
    all_pass = True
    for label, passed in targets:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  {label}: {status}")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
