"""CLI entrypoint: run the AIUC-1 ↔ OWASP Agentic Top 10 mapping pipeline.

Usage:
    python scripts/run_mapping.py [options]

Examples:
    python scripts/run_mapping.py
    python scripts/run_mapping.py --output-dir results
    python scripts/run_mapping.py --w-ref 0.50 --w-sem 0.30 --w-kw 0.20
"""

from __future__ import annotations

import argparse
import logging
import sys
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
    ctrl_mappings = sum(len(c.mappings) for c in mapping.control_level.aiuc_to_owasp)
    direct_count = sum(
        1
        for c in mapping.control_level.aiuc_to_owasp
        for m in c.mappings
        if m.confidence.value == "Direct"
    )
    related_count = ctrl_mappings - direct_count

    print("\nDone!")
    print(f"  Control-level: {ctrl_mappings} ({direct_count} Direct, {related_count} Related)")
    print(f"  Excel: {excel_path}")
    print(f"  JSON:  {json_path}")


if __name__ == "__main__":
    main()
