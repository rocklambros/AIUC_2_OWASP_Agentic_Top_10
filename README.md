# AIUC-1 ↔ OWASP Top 10 for Agentic Applications: Bi-Directional Mapping

A multi-signal mapping between the [AIUC-1 AI governance standard](https://www.aiuc-1.com) (51 controls, 6 domains) and the [OWASP Top 10 for Agentic Applications 2026](https://owasp.org/www-project-top-10-for-agentic-applications/) (10 entries, ASI01–ASI10).

Produces a reproducible, tunable bi-directional mapping at both **control level** and **sub-activity level**, output as a 4-sheet Excel workbook and structured JSON.

## Key Results

| Metric | Value |
|--------|-------|
| AIUC-1 controls mapped | 21 / 51 (41%) |
| OWASP entries with AIUC matches | 9 / 10 |
| Control-level mappings | 36 (5 Direct, 31 Related) |
| Sub-activity mappings | 129 across 132 activities |
| Anchor pair validation | 6 / 10 correct tier |

### Strongest Mappings (Direct tier)

| AIUC Control | OWASP Entry | Score |
|-------------|-------------|-------|
| D004 — Third-party testing of tool calls | ASI02 — Tool Misuse and Exploitation | 0.779 |
| E006 — Conduct vendor due diligence | ASI04 — Agentic Supply Chain Vulnerabilities | 0.752 |
| C006 — Prevent output vulnerabilities | ASI05 — Unexpected Code Execution (RCE) | 0.570 |
| E005 — Assess cloud vs on-prem processing | ASI04 — Agentic Supply Chain Vulnerabilities | 0.661 |
| C003 — Prevent harmful outputs | ASI09 — Human-Agent Trust Exploitation | 0.558 |

## Methodology

Three complementary signals are weighted into a composite score:

```
composite = 0.45 × reference_bridge + 0.35 × semantic + 0.20 × keyword
```

| Signal | Weight | Technique |
|--------|--------|-----------|
| **Reference Bridge** | 0.45 | Jaccard overlap on shared OWASP LLM Top 10 references (LLM01–LLM10) |
| **Semantic Similarity** | 0.35 | Sentence-transformer embeddings (`all-MiniLM-L6-v2`), Z-score normalized per row, sigmoid-mapped to [0,1] |
| **TF-IDF Keyword** | 0.20 | TF-IDF cosine similarity with bigrams and 24 domain-specific synonym groups |

### Confidence Tiers

| Tier | Threshold | Included in output? |
|------|-----------|---------------------|
| Direct | ≥ 0.55 | Yes |
| Related | ≥ 0.35 | Yes |
| Tangential | ≥ 0.20 | No (filtered) |
| None | < 0.20 | No |

### Relationship Types

Each mapping is annotated with a relationship type inferred from the AIUC control's classification and signal distribution:

- **Prevents** — Preventative controls
- **Detects** — Detective controls
- **Mitigates** — Strong reference bridge overlap
- **Addresses** — Strong semantic similarity
- **Partially Addresses** — Weaker signals

## Project Structure

```
├── aiuc/
│   ├── models.py              # Pydantic schemas (AIUC-1, OWASP, mapping output)
│   ├── signals.py             # 3 signal computation functions
│   ├── mapper.py              # Mapping orchestrator + anchor validation
│   ├── output.py              # Excel (4-sheet) + JSON generation
│   └── aiuc-1-standard.json   # AIUC-1 standard (51 controls, 132 activities)
│
├── owasp/
│   └── ...FINAL.json          # OWASP Top 10 for Agentic Applications 2026
│
├── mapping/                   # Generated outputs
│   ├── aiuc_owasp_mapping.xlsx
│   └── aiuc_owasp_mapping.json
│
├── scripts/
│   ├── build_aiuc_json.py     # Builds AIUC-1 JSON from scraped data
│   ├── run_scraper.py         # CLI: regenerate AIUC-1 JSON
│   └── run_mapping.py         # CLI: run mapping pipeline
│
└── pyproject.toml
```

## Quickstart

### Prerequisites

- Python 3.12+
- ~500 MB disk for sentence-transformer model (downloaded on first run)

### Install

```bash
pip install -e ".[dev]"
```

### Run the mapping pipeline

```bash
python scripts/run_mapping.py
```

Output:

```
Loading AIUC-1 from aiuc/aiuc-1-standard.json...
  Loaded 51 controls across 6 domains
Loading OWASP from owasp/...FINAL.json...
  Loaded 10 entries

Weights: ref=0.45, sem=0.35, kw=0.2
Thresholds: direct=0.55, related=0.35, tangential=0.2

Running mapping pipeline...

Done!
  Control-level: 36 (5 Direct, 31 Related)
  Excel: mapping/aiuc_owasp_mapping.xlsx
  JSON:  mapping/aiuc_owasp_mapping.json
```

### Tune parameters

All weights and thresholds are adjustable via CLI flags:

```bash
# Increase reference bridge weight, lower direct threshold
python scripts/run_mapping.py --w-ref 0.50 --w-sem 0.30 --t-direct 0.50

# Use a different embedding model
python scripts/run_mapping.py --model all-mpnet-base-v2

# Verbose logging (shows anchor pair validation)
python scripts/run_mapping.py -v
```

### Regenerate AIUC-1 JSON

```bash
python scripts/run_scraper.py
```

## Output Formats

### Excel Workbook (4 sheets)

| Sheet | Rows | Key Columns |
|-------|------|-------------|
| AIUC→OWASP (Control) | 51 AIUC controls | OWASP ID, Score, Confidence, Signal Breakdown, Relationship |
| OWASP→AIUC (Control) | 10 OWASP entries | AIUC ID, Domain, Score, Confidence, Relationship |
| AIUC→OWASP (Activity) | 132 sub-activities | OWASP ID, Score, Confidence |
| OWASP→AIUC (Activity) | 10 OWASP entries | Activity ID, Parent Control, Score, Confidence |

Styled with color-coded confidence tiers: green (Direct), yellow (Related).

### JSON Schema

```json
{
  "metadata": {
    "generated_at": "...",
    "methodology": "multi-signal-hybrid",
    "weights": { "reference_bridge": 0.45, "semantic": 0.35, "keyword": 0.20 },
    "thresholds": { "direct": 0.55, "related": 0.35, "tangential": 0.20 }
  },
  "control_level": {
    "aiuc_to_owasp": [
      {
        "aiuc_id": "D004",
        "aiuc_title": "Third-party testing of tool calls",
        "aiuc_domain": "Reliability",
        "mappings": [
          {
            "owasp_id": "ASI02",
            "owasp_title": "Tool Misuse and Exploitation",
            "score": 0.779,
            "confidence": "Direct",
            "signals": { "reference_bridge": 1.0, "semantic": 0.595, "keyword": 0.116 },
            "relationship_type": "Addresses"
          }
        ]
      }
    ],
    "owasp_to_aiuc": [ ... ]
  },
  "sub_activity_level": {
    "aiuc_to_owasp": [ ... ],
    "owasp_to_aiuc": [ ... ]
  }
}
```

## AIUC-1 Domains

| Domain | Controls | Focus |
|--------|----------|-------|
| A — Data & Privacy | A001–A007 | Data leakage, PII protection, IP rights |
| B — Security | B001–B009 | Adversarial robustness, input filtering, access control |
| C — Safety | C001–C012 | Harmful/out-of-scope outputs, vulnerability prevention |
| D — Reliability | D001–D004 | Hallucination prevention, unsafe tool call restriction |
| E — Accountability | E001–E017 | Vendor management, audit logging, regulatory compliance |
| F — Society | F001–F002 | Societal impact, responsible disclosure |

## OWASP Agentic Top 10 (2026)

| Rank | ID | Title |
|------|----|-------|
| 1 | ASI01 | Agent Goal Hijack |
| 2 | ASI02 | Tool Misuse and Exploitation |
| 3 | ASI03 | Identity and Privilege Abuse |
| 4 | ASI04 | Agentic Supply Chain Vulnerabilities |
| 5 | ASI05 | Unexpected Code Execution (RCE) |
| 6 | ASI06 | Memory & Context Poisoning |
| 7 | ASI07 | Insecure Inter-Agent Communication |
| 8 | ASI08 | Cascading Failures |
| 9 | ASI09 | Human-Agent Trust Exploitation |
| 10 | ASI10 | Rogue Agents |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Lint
ruff check aiuc/ scripts/

# Type check
mypy aiuc/ --ignore-missing-imports

# Run tests
pytest
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Data models | Pydantic 2.0+ |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Keyword similarity | scikit-learn TF-IDF |
| Excel output | openpyxl |
| Type checking | mypy (strict) |
| Linting | ruff |

## License

This project maps two publicly available security frameworks for research and governance purposes. The AIUC-1 standard is maintained at [aiuc-1.com](https://www.aiuc-1.com). The OWASP Top 10 for Agentic Applications is maintained by the [OWASP Foundation](https://owasp.org/www-project-top-10-for-agentic-applications/).
