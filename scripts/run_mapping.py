"""CLI entrypoint: run the AIUC-1 ↔ OWASP Agentic Top 10 mapping pipeline.

Usage:
    python scripts/run_mapping.py [options]

Examples:
    python scripts/run_mapping.py
    python scripts/run_mapping.py --output-dir results
    python scripts/run_mapping.py --w-ref 0.35 --w-sem 0.25 --w-kw 0.15 --w-func 0.25
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aiuc.mapper import load_aiuc, load_owasp, run_mapping  # noqa: E402
from aiuc.models import MappingThresholds, MappingWeights  # noqa: E402
from aiuc.output import generate_outputs  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run AIUC-1 ↔ OWASP Agentic Top 10 mapping pipeline",
    )
    parser.add_argument(
        "--aiuc-json",
        default="aiuc/aiuc-1-standard.json",
        help="Path to AIUC-1 standard JSON (default: aiuc/aiuc-1-standard.json)",
    )
    parser.add_argument(
        "--owasp-json",
        default="owasp/2025-OWASP-Top-10-for-Agentic-Applications-2026-12.6-1-FINAL.json",
        help="Path to OWASP Agentic Top 10 JSON",
    )
    parser.add_argument(
        "--output-dir",
        default="mapping",
        help="Output directory (default: mapping/)",
    )
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="Sentence transformer model (default: all-MiniLM-L6-v2)",
    )

    # Weight tuning
    parser.add_argument("--w-ref", type=float, default=0.35, help="Reference bridge weight")
    parser.add_argument("--w-sem", type=float, default=0.25, help="Semantic similarity weight")
    parser.add_argument("--w-kw", type=float, default=0.15, help="Keyword overlap weight")
    parser.add_argument("--w-func", type=float, default=0.25, help="Function match weight")

    # Threshold tuning
    parser.add_argument("--t-direct", type=float, default=0.55, help="Direct threshold")
    parser.add_argument("--t-related", type=float, default=0.28, help="Related threshold")
    parser.add_argument("--t-tangential", type=float, default=0.20, help="Tangential threshold")
    parser.add_argument("--t-gov-floor", type=float, default=0.22, help="Governance floor")

    parser.add_argument(
        "--validate-schema",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Validate JSON output against v2 schema (default: True)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Load data
    print(f"Loading AIUC-1 from {args.aiuc_json}...")
    aiuc = load_aiuc(args.aiuc_json)
    n_ctrls = sum(len(d.controls) for d in aiuc.domains)
    print(f"  Loaded {n_ctrls} controls across {len(aiuc.domains)} domains")

    print(f"Loading OWASP from {args.owasp_json}...")
    owasp = load_owasp(args.owasp_json)
    print(f"  Loaded {len(owasp.entries)} entries")

    weights = MappingWeights(
        reference_bridge=args.w_ref,
        semantic=args.w_sem,
        keyword=args.w_kw,
        function_match=args.w_func,
    )
    thresholds = MappingThresholds(
        direct=args.t_direct,
        related=args.t_related,
        tangential=args.t_tangential,
        governance_floor=args.t_gov_floor,
    )

    w = weights
    print(
        f"\nWeights: ref={w.reference_bridge}, sem={w.semantic}, "
        f"kw={w.keyword}, func={w.function_match}",
    )
    t = thresholds
    print(
        f"Thresholds: direct={t.direct}, related={t.related}, "
        f"tangential={t.tangential}, gov_floor={t.governance_floor}",
    )
    print("\nRunning mapping pipeline...")

    mapping = run_mapping(
        aiuc=aiuc,
        owasp=owasp,
        weights=weights,
        thresholds=thresholds,
        model_name=args.model,
    )

    # Generate outputs
    excel_path, json_path = generate_outputs(mapping, args.output_dir)

    # Summary
    all_mappings = [
        m
        for c in mapping.control_level.aiuc_to_owasp
        for m in c.mappings
    ]
    total = len(all_mappings)
    direct_count = sum(
        1 for m in all_mappings if m.confidence.value == "Direct"
    )
    primary_count = sum(
        1 for m in all_mappings if m.relevance.value == "Primary"
    )
    secondary_count = total - primary_count

    # Rationale distribution
    rationale_dist: Counter[str] = Counter(
        m.rationale_code.value for m in all_mappings
    )

    print("\nDone!")
    print(f"  Control-level: {total} mappings")
    print(f"    Confidence:  {direct_count} Direct, {total - direct_count} Related")
    print(f"    Relevance:   {primary_count} Primary, {secondary_count} Secondary")
    print(f"    Rationale:   {dict(rationale_dist.most_common())}")
    print(f"  Excel: {excel_path}")
    print(f"  JSON:  {json_path}")

    # Schema validation
    if args.validate_schema:
        schema_path = (
            Path(__file__).resolve().parent.parent
            / "schemas"
            / "crosswalk-mapping-v2.schema.json"
        )
        if schema_path.exists():
            import jsonschema

            with open(schema_path) as sf:
                schema = json.load(sf)
            with open(json_path) as df:
                data = json.load(df)
            try:
                jsonschema.validate(data, schema)
                print("  Schema validation: PASSED")
            except jsonschema.ValidationError as e:
                print(f"  Schema validation: FAILED - {e.message}")
                print(f"    Path: {list(e.absolute_path)}")
                sys.exit(1)
        else:
            print(f"  Schema validation: SKIPPED (schema not found at {schema_path})")


if __name__ == "__main__":
    main()
