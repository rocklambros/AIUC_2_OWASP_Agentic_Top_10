"""CLI entrypoint: build AIUC-1 standard JSON from scraped data.

Usage:
    python scripts/run_scraper.py [--output PATH]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json  # noqa: E402

from scripts.build_aiuc_json import build_aiuc_standard  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build AIUC-1 standard JSON")
    parser.add_argument(
        "--output",
        default="aiuc/aiuc-1-standard.json",
        help="Output JSON path (default: aiuc/aiuc-1-standard.json)",
    )
    args = parser.parse_args()

    data = build_aiuc_standard()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    n_controls = sum(len(d["controls"]) for d in data["domains"])
    n_activities = sum(
        len(c["activities"]) for d in data["domains"] for c in d["controls"]
    )
    print(f"Written {path}")
    print(f"  Domains: {len(data['domains'])}")
    print(f"  Controls: {n_controls}")
    print(f"  Activities: {n_activities}")


if __name__ == "__main__":
    main()
