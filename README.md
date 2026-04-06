# AIUC-1 ↔ OWASP Top 10 for Agentic Applications: Bi-Directional Mapping

A multi-signal mapping between the [AIUC-1 AI governance standard](https://www.aiuc-1.com) (51 controls, 6 domains) and the [OWASP Top 10 for Agentic Applications 2026](https://owasp.org/www-project-top-10-for-agentic-applications/) (10 entries, ASI01–ASI10).

Produces a reproducible, tunable bi-directional mapping at both **control level** and **sub-activity level**, output as a 5-sheet Excel workbook (with an instructional README tab) and structured JSON.

## Key Results

| Metric | Value |
|--------|-------|
| AIUC-1 controls mapped | 43 / 51 (84%) |
| OWASP entries with AIUC matches | 10 / 10 |
| Control-level mappings | 73 (27 Direct, 46 Related) |
| Rationale codes assigned | Yes (8-class taxonomy) |
| Relevance classification | Yes (Primary/Secondary) |
| Output schema | v2 (`schemas/crosswalk-mapping-v2.schema.json`) |
| Anchor pair validation | 10 / 10 correct tier |

### Strongest Mappings (Direct tier)

| AIUC Control | OWASP Entry | Score |
|-------------|-------------|-------|
| D004 — Third-party testing of tool calls | ASI02 — Tool Misuse and Exploitation | 1.000 |
| E006 — Conduct vendor due diligence | ASI04 — Agentic Supply Chain Vulnerabilities | 1.000 |
| C006 — Prevent output vulnerabilities | ASI05 — Unexpected Code Execution (RCE) | 0.817 |
| D003 — Restrict unsafe tool calls | ASI02 — Tool Misuse and Exploitation | 0.707 |
| B005 — Implement real-time input filtering | ASI01 — Agent Goal Hijack | 0.618 |

## Methodology

### The Problem: Comparing Two Frameworks That Speak Different Languages

AIUC-1 and the OWASP Agentic Top 10 were written independently by different organizations with different goals. AIUC-1 describes *controls* (what you should do), while OWASP describes *risks* (what can go wrong). They overlap conceptually but use different terminology, structure their content differently, and organize around different taxonomies.

No single technique can reliably bridge this gap. A keyword search alone would miss that "conduct vendor due diligence" (AIUC E006) addresses "agentic supply chain vulnerabilities" (ASI04) — the words barely overlap. A pure semantic model would give everything a high similarity score because all AI-security texts share common vocabulary. A reference-only approach would miss pairs that are clearly related but happen not to cite the same OWASP LLM entries.

The solution is a **multi-signal hybrid** that combines three independent evidence sources, each capturing a different kind of similarity.

### Composite Score

Three content signals are combined into a content score, then multiplied by a function-match boost:

```
content   = 0.467 × reference_bridge + 0.333 × semantic + 0.200 × keyword
composite = min(content × (1 + 0.5 × function_match), 1.0)
```

| Signal | Weight/Boost | Technique |
|--------|-------------|-----------|
| **Reference Bridge** | 0.467 | Jaccard overlap on shared OWASP LLM Top 10 references (LLM01–LLM10) |
| **Semantic Similarity** | 0.333 | Sentence-transformer embeddings (`all-MiniLM-L6-v2`), Z-score normalized per row, sigmoid-mapped to [0,1], with prevention-guideline boosting |
| **TF-IDF Keyword** | 0.200 | TF-IDF cosine similarity with bigrams and 24 domain-specific synonym groups |
| **Function Match** | ×1.5 boost | Binary: control's function class ∈ threat's function profile. Applied as 50% multiplicative uplift, not additive |

---

### Signal 1: Reference Bridge (Weight: 0.467)

#### What it measures

Both AIUC-1 and the OWASP Agentic Top 10 cite entries from the [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01–LLM10) as related vulnerabilities. When an AIUC control and an OWASP agentic entry both cite the same LLM vulnerabilities, it's strong evidence they address the same underlying problem.

#### How it works: Jaccard Similarity

The [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index) measures the overlap between two sets as the ratio of their intersection to their union:

```
                    |A ∩ B|
Jaccard(A, B) = ─────────────
                    |A ∪ B|
```

**Worked example**: AIUC control D004 cites `{LLM06}` and OWASP entry ASI02 cites `{LLM06}`. The intersection is `{LLM06}` (size 1) and the union is `{LLM06}` (size 1), so Jaccard = 1/1 = **1.0**. This is a perfect reference overlap, and indeed D004 ↔ ASI02 is the highest-scoring pair in the dataset (composite 0.779).

**Another example**: AIUC B002 cites `{LLM01, LLM08, LLM10}` and OWASP ASI06 cites `{LLM01, LLM04, LLM08}`. Intersection: `{LLM01, LLM08}` (2). Union: `{LLM01, LLM04, LLM08, LLM10}` (4). Jaccard = 2/4 = **0.5**.

#### Why this signal gets the highest weight (0.467)

The reference bridge is the most *precise* signal. If two documents independently chose to cite the same specific vulnerabilities, the authors considered them related — regardless of whether the prose uses similar words. It has very few false positives. The tradeoff is *recall*: many valid pairs don't share LLM references (either because the AIUC control has no OWASP LLM citations, or the connection is thematic rather than reference-based). The other two signals compensate for this.

#### Why Jaccard over other set similarity measures

- **Jaccard** naturally handles asymmetric set sizes and penalizes pairs that share only 1 reference out of many, which matches our intuition about relevance.
- **Dice coefficient** would double-weight intersections, being too generous for small overlaps.
- **Overlap coefficient** (`|A∩B| / min(|A|, |B|)`) would give 1.0 whenever one set is a subset, even if the superset is much larger — too permissive.

---

### Signal 2: Semantic Similarity (Weight: 0.333)

#### What it measures

How similar the *meaning* of two texts is, even when they use different words. This catches connections like "restrict unsafe tool calls" ↔ "tool misuse and exploitation" that share intent but not vocabulary.

#### How it works: Sentence-Transformer Embeddings

1. **Text assembly**: For each AIUC control, we concatenate its title, description, all activity descriptions, and keywords into a single document. For each OWASP entry, we concatenate its title, description, prevention guidelines, and examples.

2. **Embedding**: The [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) sentence-transformer model converts each text into a 384-dimensional vector (an "embedding"). Words and phrases with similar meanings get placed near each other in this vector space. The model was trained on over 1 billion sentence pairs to learn these semantic relationships.

3. **Cosine similarity**: The similarity between two embeddings is computed as the cosine of the angle between them:
   ```
                       A · B
   cosine(A, B) = ─────────────────
                   ‖A‖ × ‖B‖
   ```
   This ranges from -1 (opposite) to +1 (identical meaning). In practice, embeddings for similar domains like AI security rarely go below 0.3, which creates a problem.

#### The High-Baseline Problem and Z-Score Normalization

All AI-security documents share foundational vocabulary ("agent", "model", "security", "risk", "control"). This means raw cosine similarity between *any* AIUC control and *any* OWASP entry tends to be between 0.4 and 0.7 — the baseline is high, and the signal is in the small differences above that baseline.

To extract the signal, we apply **Z-score normalization per row** (per AIUC control):

```
                  raw_score − row_mean
z_score = ──────────────────────────────
                   row_std_dev
```

This transforms each control's scores into "how many standard deviations above (or below) average is this particular OWASP entry for this control?" A z-score of +1.5 means "this OWASP entry is much more similar to this control than the average OWASP entry."

We then map z-scores to [0, 1] using a **sigmoid function**:

```
normalized = 1 / (1 + e^(-z_score))
```

This ensures the output is bounded, with 0.5 representing "average similarity" and values above 0.5 meaning "above average for this control."

#### Why this signal gets weight 0.333

Semantic similarity captures thematic connections that reference overlap misses. It's the broadest signal — it works even when neither document cites OWASP LLM entries. However, it's less precise than reference bridge (the high-baseline problem means some noise survives normalization) and less explainable to auditors. Weight 0.333 reflects this: important but not dominant.

#### Why `all-MiniLM-L6-v2`

This model provides a good balance of speed, size (~80 MB), and quality. It's fast enough for interactive use (encodes 51 + 10 documents in under 2 seconds). The `--model` CLI flag allows substituting larger models like `all-mpnet-base-v2` for higher accuracy at the cost of speed.

---

### Signal 3: TF-IDF Keyword Similarity (Weight: 0.200)

#### What it measures

Explicit term overlap — when both documents use the same words or phrases. This catches direct terminology matches like "supply chain" ↔ "supply chain" that the other signals might underweight.

#### How it works: TF-IDF

**TF-IDF** (Term Frequency–Inverse Document Frequency) is a statistical measure of how important a word is to a document within a collection:

- **Term Frequency (TF)**: How often a word appears in a document. More occurrences = more important to that document.
- **Inverse Document Frequency (IDF)**: How rare a word is across all documents. Words appearing in every document (like "the", "security") get low IDF; distinctive words (like "hallucination", "sandbox") get high IDF.
- **TF-IDF = TF × IDF**: A word is important if it appears frequently in *this* document but rarely in *others*. This naturally downweights generic AI-security vocabulary.

We use `sublinear_tf=True`, which applies logarithmic dampening to term frequency (`1 + log(TF)` instead of raw `TF`). This prevents a word mentioned 10 times from being 10× more important than one mentioned once — the first mention matters most.

#### Bigrams (ngram_range=(1,2))

We include both single words and two-word phrases. This matters because "tool call" is more specific than "tool" or "call" individually, and "prompt injection" is a specific concept that should match as a unit.

#### Domain-Specific Synonym Expansion

A critical challenge: AIUC might say "vendor due diligence" while OWASP says "supply chain." These mean similar things but share no words. We address this with 24 manually curated synonym groups:

```python
{"supply chain", "third party", "dependency", "vendor", "third-party"}
{"prompt injection", "adversarial input", "adversarial prompt", "goal hijack"}
{"tool call", "tool misuse", "tool invocation", "tool use", "tool execution"}
...
```

When a document contains any term from a group, all other terms in that group are appended to the text before TF-IDF computation. This bridges vocabulary gaps without relying on an ML model.

#### Cosine Similarity on TF-IDF Vectors

After converting each document into a TF-IDF vector (with 5,000 max features), we compute cosine similarity between AIUC and OWASP vectors. The result is a score from 0 (no term overlap) to 1 (identical term distribution).

#### Why this signal gets the lowest weight (0.200)

Keyword matching is brittle — it rewards surface-level word overlap without understanding meaning. Two documents about completely different topics can score high if they share generic terms. It also can't catch paraphrases or conceptual equivalences beyond the 24 synonym groups. However, it provides a useful "sanity check" and catches cases where the semantic model's normalization accidentally suppresses a genuine keyword match. Weight 0.200 keeps it contributory but not decisive.

---

### Signal 4: Function Match (Boost: ×1.5)

#### What it measures

Whether a control's *defense function* is relevant to a specific threat. This uses domain knowledge encoded in the control-function taxonomy (`aiuc/taxonomy.py`) rather than text analysis.

#### How it works: Control-Function Taxonomy

Each control is assigned one of 8 function classes (PREV, SCOPE, GATE, DETECT, VALID, GOVERN, ISOLATE, DISCLOSE) based on its defense role. Each OWASP threat has a function profile listing which classes are relevant. For example, ASI01 (Agent Goal Hijack) is addressed by PREV, SCOPE, GATE, VALID, DETECT, and GOVERN controls.

For each (control, threat) pair:
- Look up the control's function class from `AIUC_CONTROL_FUNCTIONS`
- Look up the threat's applicable classes from `THREAT_FUNCTION_PROFILES`
- If the control's class is in the threat's profile: `function_match = 1.0`, else `0.0`

#### Why multiplicative (not additive)

Function match is a **confidence amplifier**, not evidence. It answers "is this *type* of control relevant to this threat?" — a necessary but not sufficient condition. Adding it as a 4th weighted signal (as in early versions) created a score floor: every function-matched control cleared the threshold regardless of content evidence, producing hundreds of false positives.

The multiplicative approach (`content × 1.5`) ensures that function match can *boost* a genuine content match but cannot *create* one from nothing. A control with zero reference overlap and average semantic similarity stays below threshold even with function match = 1.0.

---

### Why These Four Signals (and Not Others)

The four signals were chosen to be **complementary along different dimensions**:

| Dimension | Reference Bridge | Semantic | Keyword | Function Match |
|-----------|-----------------|----------|---------|----------------|
| Evidence type | Structural (shared citations) | Meaning (NLP) | Lexical (exact terms) | Structural (control function) |
| Precision | Very high | Medium | Low–medium | High |
| Recall | Low (many pairs lack shared refs) | High | Medium | High |
| Explainability | High (auditors can verify) | Low (black-box model) | Medium | High |
| Failure mode | Misses pairs without LLM refs | High baseline noise | Surface-level false matches | Over-maps cross-cutting controls |

Each signal's weakness is another signal's strength. Reference bridge is precise but narrow; semantic is broad but noisy; keyword is transparent but shallow; function match provides structural domain knowledge but can't distinguish specific vs generic relevance within a function class. The multiplicative combination outperforms any individual signal.

**Signals considered but not used:**
- **Citation co-occurrence** (beyond LLM Top 10): The two frameworks cite different standards (AIUC cites EU AI Act, NIST; OWASP cites ATLAS, SAIF). Too sparse to be useful.
- **Structural similarity** (control hierarchy matching): The frameworks organize differently (domains vs. ranked list). No structural alignment to exploit.
- **LLM-based classification** (ask an LLM to judge relatedness): Would introduce model bias and non-reproducibility. Deliberately avoided for a mapping meant to be auditable and deterministic.

---

### Confidence Tiers

| Tier | Threshold | Included in output? | Meaning |
|------|-----------|---------------------|---------|
| Direct | ≥ 0.55 | Yes (green) | Strong evidence from multiple signals |
| Related (Primary) | ≥ 0.35 | Yes (yellow) | Meaningful connection for Primary-classified mappings |
| Related (Secondary) | ≥ 0.50 | Yes (yellow) | Meaningful connection for Secondary-classified mappings (higher evidence bar) |
| Tangential | ≥ 0.20 | No (filtered) | Weak connection, likely coincidental overlap |
| None | < 0.20 | No | No meaningful connection |

**Governance floor**: GOVERN and DISCLOSE controls with `function_match = 1.0` that are classified as Primary are promoted to Related at a lower threshold of **0.22**. These controls have structurally generic text (policy language) that produces weak content signals across all standards — the floor ensures they aren't systematically excluded when domain knowledge confirms their relevance.

#### How the Thresholds Were Calibrated

The thresholds are calibrated against **10 anchor pairs** where a domain expert manually assessed the expected tier. All 10 match their expected tier.

```python
# Example anchor pairs from mapper.py
{"aiuc": "D004", "owasp": "ASI02", "expected": "Direct"},   # Perfect ref overlap
{"aiuc": "E006", "owasp": "ASI04", "expected": "Direct"},   # Perfect ref overlap
{"aiuc": "B001", "owasp": "ASI01", "expected": "Related"},  # Jaccard 1/4
{"aiuc": "B002", "owasp": "ASI06", "expected": "Direct"},   # Strong ref + func boost
```

The **relevance-aware threshold** design reflects the principle that Primary mappings (which the classification layer identifies with 100% rationale accuracy) need less content evidence than Secondary mappings. This avoids both over-inclusion of weakly-supported Secondary pairs and under-inclusion of structurally important Primary pairs.

All thresholds are tunable via CLI flags (`--t-direct`, `--t-related`, `--t-sec-related`, `--t-tangential`, `--t-gov-floor`).

---

### Relationship Types

Each mapping is annotated with a relationship type inferred from the AIUC control's classification and signal distribution:

| Type | Inference Rule | Meaning for Governance |
|------|---------------|----------------------|
| **Prevents** | AIUC control type contains "preventative" or "preventive" | The control proactively stops the risk from occurring |
| **Detects** | AIUC control type contains "detective" | The control identifies when the risk is being exploited |
| **Mitigates** | Reference bridge sub-score > 0.6 | Strong shared-reference evidence that the control reduces risk impact |
| **Addresses** | Semantic sub-score > 0.6 | The control is thematically aligned with the risk |
| **Partially Addresses** | Default (none of the above) | The control has some relevance but incomplete coverage |

The inference is hierarchical: control metadata (if available) takes priority over signal-based inference. This ensures that AIUC controls explicitly classified as preventative or detective are labeled accurately, while the signal-based rules handle the majority of mappings where control type metadata is not specific enough.

---

### Rationale and Relevance Classification

Every mapping carries a **rationale code** (why the mapping exists) and a **relevance level** (how directly it mitigates the threat). These are computed deterministically by `aiuc/taxonomy.py`.

#### Rationale Taxonomy (8 classes)

| Code | Label | Definition |
|------|-------|------------|
| PREV | Prevent | Directly blocks the core attack mechanism |
| SCOPE | Constrain scope | Limits blast radius after compromise |
| GATE | Human gate | Enforces human approval or intervention |
| DETECT | Detect and trace | Runtime detection or forensic traceability |
| VALID | Validate and test | Tests or audits that other controls work |
| GOVERN | Policy and governance | Organizational policy or accountability |
| ISOLATE | Isolate and contain | Architectural separation preventing propagation |
| DISCLOSE | Disclose and calibrate | Transparency enabling trust calibration |

Each control is assigned exactly one function class. The assignment is static for AIUC-1 (`AIUC_CONTROL_FUNCTIONS` in taxonomy.py) and keyword-based for new standards (`FUNCTION_KEYWORDS`).

#### Primary/Secondary Classification

Relevance is determined per (control, threat) pair using threat-specific profiles (`THREAT_PROFILES` in taxonomy.py). The rules include:

- **Function-class match**: If the control's function class is in the threat's `primary_functions` set → Primary
- **Topic match**: If the control's title matches any of the threat's `primary_topics` regexes → Primary
- **DETECT subcategory**: Each threat specifies a `detect_rule` (all, generic_only, specific_only, never) that determines whether DETECT controls are Primary or Secondary
- **DISCLOSE handling**: Only specific DISCLOSE controls listed in `disclose_primary` are Primary
- **Default**: Secondary

#### Validation Results

| Dataset | Standard | Mappings | Rationale Accuracy | Relevance Accuracy |
|---------|----------|----------|-------------------|-------------------|
| Training | AIUC-1 | 119 | 100.0% | 99.2% |
| Validation | NIST AI RMF 1.0 | 66 | 100.0% | 84.8% |
| Generalization gap | — | — | 0.0% | 14.3% |

Run `pytest tests/test_classification.py -v` to verify. See `tests/test_data.json` for ground truth.

---

### Output Schema (v2)

The pipeline output conforms to `schemas/crosswalk-mapping-v2.schema.json`, validated on every run.

**Key design decisions:**
- **Standard-agnostic field names**: `control_id` / `domain` instead of `aiuc_id` / `aiuc_domain` — the same schema validates NIST, ISO, or EU AI Act mappings
- **Score and signals are optional**: Required for diagnostic output; omit for published crosswalks
- **Function coverage per threat**: Each OWASP entry reports how many controls cover each rationale code, highlighting defense-in-depth gaps
- **Gap analysis**: Unmapped controls are listed with a `gap_reason` explaining why

See [schemas/README.md](schemas/README.md) for full documentation, rationale taxonomy definitions, and validation instructions.

The `--validate-schema` flag (default: on) runs jsonschema validation after every pipeline run. Use `--no-validate-schema` to skip.

## Project Structure

```
├── aiuc/
│   ├── models.py              # Pydantic schemas (v1 + v2 crosswalk models)
│   ├── taxonomy.py            # Control-function taxonomy and classification rules
│   ├── signals.py             # 4 signal computation (3 content + multiplicative boost)
│   ├── mapper.py              # Mapping orchestrator + anchor validation
│   ├── output.py              # Excel (5-sheet) + v2 JSON generation
│   └── aiuc-1-standard.json   # AIUC-1 standard (51 controls, 132 activities)
│
├── schemas/
│   ├── crosswalk-mapping-v2.schema.json  # v2 output JSON Schema
│   └── README.md              # Schema documentation + rationale taxonomy
│
├── owasp/
│   └── ...FINAL.json          # OWASP Top 10 for Agentic Applications 2026
│
├── mapping/                   # Generated outputs
│   ├── aiuc_owasp_mapping.xlsx
│   └── aiuc_owasp_mapping.json
│
├── tests/
│   ├── test_classification.py # Rationale + relevance test harness
│   ├── test_data.json         # 119 AIUC training + 66 NIST validation mappings
│   └── test_readme_sheet.py   # Excel README sheet tests
│
├── scripts/
│   ├── build_aiuc_json.py     # Builds AIUC-1 JSON from scraped data
│   ├── run_scraper.py         # CLI: regenerate AIUC-1 JSON
│   ├── run_mapping.py         # CLI: run mapping pipeline
│   └── evaluate_pipeline.py   # Pipeline recall/precision evaluation
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
Weights: ref=0.467, sem=0.333, kw=0.2, boost=0.5
Thresholds: direct=0.55, related=0.35, tangential=0.2, gov_floor=0.22

Done!
  Control-level: 73 mappings
    Confidence:  27 Direct, 46 Related
    Relevance:   51 Primary, 22 Secondary
  Schema validation: PASSED
```

### Tune parameters

All weights and thresholds are adjustable via CLI flags:

```bash
# Adjust content weights and function boost
python scripts/run_mapping.py --w-ref 0.50 --w-sem 0.30 --w-kw 0.20 --w-boost 0.5

# Use a different embedding model
python scripts/run_mapping.py --model all-mpnet-base-v2

# Adjust relevance-aware thresholds
python scripts/run_mapping.py --t-related 0.35 --t-sec-related 0.50 --t-gov-floor 0.22

# Verbose logging (shows anchor pair validation)
python scripts/run_mapping.py -v

# Skip schema validation
python scripts/run_mapping.py --no-validate-schema
```

### Regenerate AIUC-1 JSON

```bash
python scripts/run_scraper.py
```

## Output Formats

### Excel Workbook (5 sheets)

| Sheet | Rows | Key Columns |
|-------|------|-------------|
| README | — | Rationale taxonomy, relevance classification, scoring methodology, confidence tiers, framework glossaries |
| AIUC→OWASP (Control) | 51 AIUC controls | Function Class, Rationale, Relevance, Score, Confidence, Signal Breakdown |
| OWASP→AIUC (Control) | 10 OWASP entries | Function Coverage, Uncovered Functions, Rationale, Relevance, Score, Confidence |
| AIUC→OWASP (Activity) | 132 sub-activities | OWASP ID, Score, Confidence |
| OWASP→AIUC (Activity) | 10 OWASP entries | Activity ID, Parent Control, Score, Confidence |

Styled with color-coded confidence tiers (green=Direct, yellow=Related) and relevance (blue=Primary, gray=Secondary).

### JSON Output (v2 Schema)

The JSON output conforms to `schemas/crosswalk-mapping-v2.schema.json`. Key sections:

```json
{
  "metadata": {
    "schema_version": "2.0",
    "source_standard": { "name": "AIUC-1", "version": "1.0", "controls": 51 },
    "target_standard": { "name": "OWASP Top 10 for Agentic Applications", "version": "2026" },
    "pipeline": { "signals": { ... }, "thresholds": { ... } },
    "classification": { "rationale_taxonomy": { ... }, "classification_accuracy": { ... } }
  },
  "summary": {
    "controls_mapped": "43 / 51",
    "total_mappings": 73,
    "primary_mappings": 51,
    "secondary_mappings": 22,
    "rationale_distribution": { "SCOPE": 19, "PREV": 16, ... }
  },
  "control_level": {
    "source_to_owasp": [
      {
        "control_id": "D004",
        "control_title": "Third-party testing of tool calls",
        "domain": "Reliability",
        "function_class": "VALID",
        "mappings": [
          {
            "owasp_id": "ASI02",
            "relevance": "Primary",
            "rationale_code": "VALID",
            "rationale_label": "Validate and test",
            "score": 1.0,
            "signals": { "reference_bridge": 1.0, "semantic": 0.672, "keyword": 0.142 }
          }
        ]
      }
    ],
    "owasp_to_source": [ ... ]
  },
  "gap_analysis": {
    "unmapped_controls": [ ... ],
    "unmapped_count": 8
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
| Data models | Pydantic 2.0+ (v1 + v2 crosswalk schema) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Keyword similarity | scikit-learn TF-IDF |
| Excel output | openpyxl |
| Type checking | mypy (strict) |
| Linting | ruff |

## License

This project maps two publicly available security frameworks for research and governance purposes. The AIUC-1 standard is maintained at [aiuc-1.com](https://www.aiuc-1.com). The OWASP Top 10 for Agentic Applications is maintained by the [OWASP Foundation](https://owasp.org/www-project-top-10-for-agentic-applications/).
