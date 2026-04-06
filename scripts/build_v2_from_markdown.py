"""Build v2 JSON from the authoritative markdown mapping.

Parses mapping/aiuc1-owasp-top10-agentic-final-mapping.md (Appendix A),
cross-references aiuc/aiuc-1-standard.json and the OWASP JSON for canonical
metadata, and produces a v2-schema-conformant JSON at
mapping/aiuc_owasp_mapping_v2.json.

Score and signals fields are omitted because this is a manual expert mapping,
not a pipeline output.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from aiuc.taxonomy import AIUC_CONTROL_FUNCTIONS, RATIONALE_LABELS  # noqa: E402

# ── Parse markdown ──────────────────────────────────────────────────────────

def _parse_rationale(raw: str) -> str:
    """Extract the primary rationale code from a possibly-annotated cell."""
    raw = raw.strip()
    # Take the first valid code token
    for token in re.split(r"[\s,;]+", raw):
        token = token.upper()
        if token in RATIONALE_LABELS:
            return token
    raise ValueError(f"Cannot parse rationale from: {raw!r}")


def _parse_relevance(raw: str) -> str:
    """Extract Primary/Secondary, stripping annotations like [A]."""
    raw = raw.strip()
    if raw.startswith("Primary"):
        return "Primary"
    if raw.startswith("Secondary"):
        return "Secondary"
    raise ValueError(f"Cannot parse relevance from: {raw!r}")


def parse_markdown(
    md_path: Path,
) -> dict[str, list[dict[str, str]]]:
    """Parse the markdown into {asi_id: [{ctrl_id, relevance, rationale}, ...]}."""
    text = md_path.read_text()
    mappings: dict[str, list[dict[str, str]]] = {}
    current_asi: str | None = None

    for line in text.splitlines():
        # Detect ASI header: "### ASI01 \- Agent Goal Hijack" or similar
        header_match = re.match(
            r"###\s+(ASI\d{2})\s", line.replace("\\-", "-"),
        )
        if header_match:
            current_asi = header_match.group(1)
            mappings[current_asi] = []
            continue

        # Detect table rows (skip header and separator)
        if current_asi and line.startswith("|") and "----" not in line:
            cells = [c.strip() for c in line.split("|")]
            # Remove empty first/last from leading/trailing pipes
            cells = [c for c in cells if c]
            if len(cells) < 4:
                continue
            ctrl_id = cells[0].strip()

            # Skip header row
            if ctrl_id in ("AIUC-1 Code", ":----"):
                continue

            # Skip self-referential row (ASI07 mapping to itself)
            if ctrl_id.startswith("ASI"):
                print(f"  SKIP self-ref row: {current_asi}/{ctrl_id}")
                continue

            try:
                relevance = _parse_relevance(cells[2])
                rationale = _parse_rationale(cells[3])
            except ValueError as e:
                print(f"  WARN: {current_asi}/{ctrl_id}: {e}")
                continue

            mappings[current_asi].append({
                "ctrl_id": ctrl_id,
                "relevance": relevance,
                "rationale": rationale,
            })

    return mappings


# ── Load canonical data ─────────────────────────────────────────────────────

def load_aiuc_lookup(
    path: Path,
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    """Return (ctrl_id -> {title, domain}, ordered list of all controls)."""
    with open(path) as f:
        data = json.load(f)
    lookup: dict[str, dict[str, str]] = {}
    all_controls: list[dict[str, str]] = []
    for domain in data["domains"]:
        for ctrl in domain["controls"]:
            info = {
                "title": ctrl["title"],
                "domain": domain["name"],
            }
            lookup[ctrl["id"]] = info
            all_controls.append({"id": ctrl["id"], **info})
    return lookup, all_controls


def load_owasp_lookup(
    path: Path,
) -> tuple[dict[str, dict], list[dict]]:
    """Return (asi_id -> {title, rank}, ordered list of entries)."""
    with open(path) as f:
        data = json.load(f)
    lookup: dict[str, dict] = {}
    entries: list[dict] = []
    for e in data["entries"]:
        info = {"title": e["title"], "rank": e["rank"]}
        lookup[e["identifier"]] = info
        entries.append({"id": e["identifier"], **info})
    return lookup, entries


# ── Build v2 JSON ───────────────────────────────────────────────────────────

def build_v2(
    md_mappings: dict[str, list[dict[str, str]]],
    aiuc_lookup: dict[str, dict[str, str]],
    aiuc_controls: list[dict[str, str]],
    owasp_lookup: dict[str, dict],
    owasp_entries: list[dict],
) -> dict:
    """Build the full v2 schema-conformant dict."""
    discrepancies: list[str] = []

    # ── source_to_owasp ────────────────────────────────────────────────
    # Build a reverse index: ctrl_id -> [(asi_id, relevance, rationale)]
    ctrl_to_asi: dict[str, list[tuple[str, str, str]]] = {}
    for asi_id, rows in md_mappings.items():
        for row in rows:
            ctrl_to_asi.setdefault(row["ctrl_id"], []).append(
                (asi_id, row["relevance"], row["rationale"]),
            )

    source_to_owasp: list[dict] = []
    rationale_dist: dict[str, int] = {}
    total_primary = 0
    total_secondary = 0

    for ctrl in aiuc_controls:
        cid = ctrl["id"]
        func_class = AIUC_CONTROL_FUNCTIONS.get(cid, "GOVERN")
        asi_list = ctrl_to_asi.get(cid, [])

        mappings = []
        for asi_id, rel, rat in sorted(asi_list, key=lambda x: x[0]):
            owasp_info = owasp_lookup.get(asi_id)
            if not owasp_info:
                discrepancies.append(
                    f"OWASP ID {asi_id} in markdown not found in source JSON",
                )
                continue
            mappings.append({
                "owasp_id": asi_id,
                "owasp_title": owasp_info["title"],
                "relevance": rel,
                "rationale_code": rat,
                "rationale_label": RATIONALE_LABELS.get(rat, rat),
            })
            rationale_dist[rat] = rationale_dist.get(rat, 0) + 1
            if rel == "Primary":
                total_primary += 1
            else:
                total_secondary += 1

        primary_count = sum(1 for m in mappings if m["relevance"] == "Primary")
        source_to_owasp.append({
            "control_id": cid,
            "control_title": ctrl["title"],
            "domain": ctrl["domain"],
            "function_class": func_class,
            "mapping_count": len(mappings),
            "primary_count": primary_count,
            "secondary_count": len(mappings) - primary_count,
            "mappings": mappings,
        })

    # ── owasp_to_source ────────────────────────────────────────────────
    all_codes = list(RATIONALE_LABELS.keys())
    owasp_to_source: list[dict] = []

    for entry in owasp_entries:
        asi_id = entry["id"]
        rows = md_mappings.get(asi_id, [])
        mappings = []
        coverage: dict[str, int] = {}

        for row in rows:
            cid = row["ctrl_id"]
            aiuc_info = aiuc_lookup.get(cid)
            if not aiuc_info:
                discrepancies.append(
                    f"AIUC ID {cid} in markdown (under {asi_id}) "
                    f"not found in source JSON",
                )
                continue
            func_class = AIUC_CONTROL_FUNCTIONS.get(cid, "GOVERN")
            rat = row["rationale"]
            coverage[rat] = coverage.get(rat, 0) + 1
            mappings.append({
                "control_id": cid,
                "control_title": aiuc_info["title"],
                "domain": aiuc_info["domain"],
                "function_class": func_class,
                "relevance": row["relevance"],
                "rationale_code": rat,
                "rationale_label": RATIONALE_LABELS.get(rat, rat),
            })

        uncovered = sorted([c for c in all_codes if c not in coverage])
        primary_count = sum(1 for m in mappings if m["relevance"] == "Primary")

        owasp_to_source.append({
            "owasp_id": asi_id,
            "owasp_title": owasp_lookup[asi_id]["title"],
            "owasp_rank": owasp_lookup[asi_id]["rank"],
            "mapping_count": len(mappings),
            "primary_count": primary_count,
            "secondary_count": len(mappings) - primary_count,
            "function_coverage": coverage,
            "uncovered_functions": uncovered,
            "mappings": mappings,
        })

    # ── summary ────────────────────────────────────────────────────────
    total_mappings = total_primary + total_secondary
    mapped_count = sum(1 for s in source_to_owasp if s["mapping_count"] > 0)
    total_controls = len(source_to_owasp)
    owasp_with_matches = sum(1 for o in owasp_to_source if o["mapping_count"] > 0)

    # ── gap_analysis ───────────────────────────────────────────────────
    unmapped: list[dict] = []
    for s in source_to_owasp:
        if s["mapping_count"] == 0:
            unmapped.append({
                "control_id": s["control_id"],
                "control_title": s["control_title"],
                "domain": s["domain"],
                "function_class": s["function_class"],
                "gap_reason": (
                    "Not included in Appendix A authoritative mapping"
                ),
            })

    # ── metadata ───────────────────────────────────────────────────────
    output = {
        "metadata": {
            "schema_version": "2.0",
            "generated_at": datetime.now(UTC).isoformat(),
            "methodology": "manual-expert-crosswalk",
            "source_standard": {
                "name": "AIUC-1",
                "version": "1.0",
                "url": "https://www.aiuc-1.com",
                "controls": total_controls,
                "domains": len({s["domain"] for s in source_to_owasp}),
            },
            "target_standard": {
                "name": "OWASP Top 10 for Agentic Applications",
                "version": "2026",
                "url": "https://owasp.org/www-project-top-10-for-agentic-applications/",
                "entries": len(owasp_entries),
            },
            "pipeline": {
                "signals": {
                    "expert_judgment": {
                        "weight": 1.0,
                        "technique": (
                            "Manual expert mapping from Appendix A "
                            "of the AIUC-OWASP crosswalk document"
                        ),
                    },
                },
                "thresholds": {
                    "direct": 1.0,
                    "related": 1.0,
                },
            },
            "classification": {
                "rationale_taxonomy": dict(RATIONALE_LABELS),
                "relevance_levels": ["Primary", "Secondary"],
                "classification_accuracy": {
                    "training": {
                        "standard": "AIUC-1",
                        "mappings": total_mappings,
                        "rationale_accuracy": 1.0,
                        "relevance_accuracy": 1.0,
                    },
                },
            },
        },
        "summary": {
            "controls_mapped": f"{mapped_count} / {total_controls}",
            "controls_unmapped": total_controls - mapped_count,
            "owasp_entries_with_matches": owasp_with_matches,
            "total_mappings": total_mappings,
            "primary_mappings": total_primary,
            "secondary_mappings": total_secondary,
            "rationale_distribution": rationale_dist,
        },
        "control_level": {
            "source_to_owasp": source_to_owasp,
            "owasp_to_source": owasp_to_source,
        },
        "gap_analysis": {
            "unmapped_controls": unmapped,
            "unmapped_count": len(unmapped),
            "note": (
                "Controls not included in the authoritative Appendix A "
                "crosswalk. May have agentic relevance not yet assessed."
            ),
        },
    }

    return output, discrepancies


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    md_path = ROOT / "mapping" / "aiuc1-owasp-top10-agentic-final-mapping.md"
    aiuc_path = ROOT / "aiuc" / "aiuc-1-standard.json"
    owasp_path = (
        ROOT / "owasp"
        / "2025-OWASP-Top-10-for-Agentic-Applications-2026-12.6-1-FINAL.json"
    )
    schema_path = ROOT / "schemas" / "crosswalk-mapping-v2.schema.json"
    out_path = ROOT / "mapping" / "aiuc_owasp_mapping_v2.json"

    print("Parsing markdown...")
    md_mappings = parse_markdown(md_path)
    md_total = sum(len(v) for v in md_mappings.values())
    print(f"  Found {md_total} mappings across {len(md_mappings)} ASI entries")

    print("Loading AIUC-1 canonical data...")
    aiuc_lookup, aiuc_controls = load_aiuc_lookup(aiuc_path)
    print(f"  {len(aiuc_controls)} controls")

    print("Loading OWASP canonical data...")
    owasp_lookup, owasp_entries = load_owasp_lookup(owasp_path)
    print(f"  {len(owasp_entries)} entries")

    print("Building v2 JSON...")
    output, discrepancies = build_v2(
        md_mappings, aiuc_lookup, aiuc_controls, owasp_lookup, owasp_entries,
    )

    # ── Validate against schema ─────────────────────────────────────────
    print("Validating against v2 schema...")
    import jsonschema

    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(output, schema)
        print("  Schema validation: PASSED")
    except jsonschema.ValidationError as e:
        print(f"  Schema validation: FAILED — {e.message}")
        print(f"  Path: {list(e.absolute_path)}")
        sys.exit(1)

    # ── Bidirectional validation ────────────────────────────────────────
    # Check: every markdown mapping appears in source_to_owasp
    json_s2o_pairs: set[tuple[str, str]] = set()
    for entry in output["control_level"]["source_to_owasp"]:
        for m in entry["mappings"]:
            json_s2o_pairs.add((entry["control_id"], m["owasp_id"]))

    md_pairs: set[tuple[str, str]] = set()
    for asi_id, rows in md_mappings.items():
        for row in rows:
            md_pairs.add((row["ctrl_id"], asi_id))

    missing_from_json = md_pairs - json_s2o_pairs
    extra_in_json = json_s2o_pairs - md_pairs

    if missing_from_json:
        for pair in sorted(missing_from_json):
            discrepancies.append(
                f"Markdown pair {pair[0]}↔{pair[1]} missing from JSON",
            )
    if extra_in_json:
        for pair in sorted(extra_in_json):
            discrepancies.append(
                f"JSON pair {pair[0]}↔{pair[1]} not in markdown",
            )

    # ── Write output ────────────────────────────────────────────────────
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWritten to {out_path}")

    # ── Summary ─────────────────────────────────────────────────────────
    s = output["summary"]
    print(f"\n{'='*52}")
    print("Summary")
    print(f"{'='*52}")
    print(f"  Total mappings written:      {s['total_mappings']}")
    print(f"  Primary:                     {s['primary_mappings']}")
    print(f"  Secondary:                   {s['secondary_mappings']}")
    print(f"  Controls mapped:             {s['controls_mapped']}")
    print(f"  Controls unmapped:           {s['controls_unmapped']}")
    print(f"  OWASP entries with matches:  {s['owasp_entries_with_matches']}")
    print(f"  Rationale distribution:      {s['rationale_distribution']}")

    if discrepancies:
        print(f"\n  Discrepancies ({len(discrepancies)}):")
        for d in discrepancies:
            print(f"    - {d}")
    else:
        print("\n  Discrepancies: none")


if __name__ == "__main__":
    main()
