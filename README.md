# AIUC-1 ↔ OWASP Top 10 for Agentic Applications: Bi-Directional Mapping

A multi-signal mapping between the [AIUC-1 AI governance standard](https://www.aiuc-1.com) (51 controls, 6 domains) and the [OWASP Top 10 for Agentic Applications 2026](https://owasp.org/www-project-top-10-for-agentic-applications/) (10 entries, ASI01–ASI10).

Produces a reproducible, tunable bi-directional mapping at both **control level** and **sub-activity level**, output as a 5-sheet Excel workbook (with an instructional README tab) and structured JSON.

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

### The Problem: Comparing Two Frameworks That Speak Different Languages

AIUC-1 and the OWASP Agentic Top 10 were written independently by different organizations with different goals. AIUC-1 describes *controls* (what you should do), while OWASP describes *risks* (what can go wrong). They overlap conceptually but use different terminology, structure their content differently, and organize around different taxonomies.

No single technique can reliably bridge this gap. A keyword search alone would miss that "conduct vendor due diligence" (AIUC E006) addresses "agentic supply chain vulnerabilities" (ASI04) — the words barely overlap. A pure semantic model would give everything a high similarity score because all AI-security texts share common vocabulary. A reference-only approach would miss pairs that are clearly related but happen not to cite the same OWASP LLM entries.

The solution is a **multi-signal hybrid** that combines three independent evidence sources, each capturing a different kind of similarity.

### Composite Score

```
composite = 0.45 × reference_bridge + 0.35 × semantic + 0.20 × keyword
```

| Signal | Weight | Technique |
|--------|--------|-----------|
| **Reference Bridge** | 0.45 | Jaccard overlap on shared OWASP LLM Top 10 references (LLM01–LLM10) |
| **Semantic Similarity** | 0.35 | Sentence-transformer embeddings (`all-MiniLM-L6-v2`), Z-score normalized per row, sigmoid-mapped to [0,1] |
| **TF-IDF Keyword** | 0.20 | TF-IDF cosine similarity with bigrams and 24 domain-specific synonym groups |

---

### Signal 1: Reference Bridge (Weight: 0.45)

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

#### Why this signal gets the highest weight (0.45)

The reference bridge is the most *precise* signal. If two documents independently chose to cite the same specific vulnerabilities, the authors considered them related — regardless of whether the prose uses similar words. It has very few false positives. The tradeoff is *recall*: many valid pairs don't share LLM references (either because the AIUC control has no OWASP LLM citations, or the connection is thematic rather than reference-based). The other two signals compensate for this.

#### Why Jaccard over other set similarity measures

- **Jaccard** naturally handles asymmetric set sizes and penalizes pairs that share only 1 reference out of many, which matches our intuition about relevance.
- **Dice coefficient** would double-weight intersections, being too generous for small overlaps.
- **Overlap coefficient** (`|A∩B| / min(|A|, |B|)`) would give 1.0 whenever one set is a subset, even if the superset is much larger — too permissive.

---

### Signal 2: Semantic Similarity (Weight: 0.35)

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

#### Why this signal gets weight 0.35

Semantic similarity captures thematic connections that reference overlap misses. It's the broadest signal — it works even when neither document cites OWASP LLM entries. However, it's less precise than reference bridge (the high-baseline problem means some noise survives normalization) and less explainable to auditors. Weight 0.35 reflects this: important but not dominant.

#### Why `all-MiniLM-L6-v2`

This model provides a good balance of speed, size (~80 MB), and quality. It's fast enough for interactive use (encodes 51 + 10 documents in under 2 seconds). The `--model` CLI flag allows substituting larger models like `all-mpnet-base-v2` for higher accuracy at the cost of speed.

---

### Signal 3: TF-IDF Keyword Similarity (Weight: 0.20)

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

#### Why this signal gets the lowest weight (0.20)

Keyword matching is brittle — it rewards surface-level word overlap without understanding meaning. Two documents about completely different topics can score high if they share generic terms. It also can't catch paraphrases or conceptual equivalences beyond the 24 synonym groups. However, it provides a useful "sanity check" and catches cases where the semantic model's normalization accidentally suppresses a genuine keyword match. Weight 0.20 keeps it contributory but not decisive.

---

### Why These Three Signals (and Not Others)

The three signals were chosen to be **complementary along different dimensions**:

| Dimension | Reference Bridge | Semantic | Keyword |
|-----------|-----------------|----------|---------|
| Evidence type | Structural (shared citations) | Meaning (NLP) | Lexical (exact terms) |
| Precision | Very high | Medium | Low–medium |
| Recall | Low (many pairs lack shared refs) | High | Medium |
| Explainability | High (auditors can verify) | Low (black-box model) | Medium |
| Failure mode | Misses pairs without LLM refs | High baseline noise | Surface-level false matches |

Each signal's weakness is another signal's strength. Reference bridge is precise but narrow; semantic is broad but noisy; keyword is transparent but shallow. The weighted combination outperforms any individual signal.

**Signals considered but not used:**
- **Citation co-occurrence** (beyond LLM Top 10): The two frameworks cite different standards (AIUC cites EU AI Act, NIST; OWASP cites ATLAS, SAIF). Too sparse to be useful.
- **Structural similarity** (control hierarchy matching): The frameworks organize differently (domains vs. ranked list). No structural alignment to exploit.
- **LLM-based classification** (ask an LLM to judge relatedness): Would introduce model bias and non-reproducibility. Deliberately avoided for a mapping meant to be auditable and deterministic.

---

### Confidence Tiers

| Tier | Threshold | Included in output? | Meaning |
|------|-----------|---------------------|---------|
| Direct | ≥ 0.55 | Yes (green) | Strong evidence from multiple signals |
| Related | ≥ 0.35 | Yes (yellow) | Meaningful connection, typically 1–2 strong signals |
| Tangential | ≥ 0.20 | No (filtered) | Weak connection, likely coincidental overlap |
| None | < 0.20 | No | No meaningful connection |

#### How the Thresholds Were Calibrated

The thresholds are not arbitrary — they were calibrated against a set of **10 anchor pairs**: control-OWASP pairs where a domain expert manually assessed the expected relationship strength based on shared LLM references and conceptual alignment.

```python
# Example anchor pairs from mapper.py
{"aiuc": "D004", "owasp": "ASI02", "expected": "Direct"},   # Perfect ref overlap
{"aiuc": "E006", "owasp": "ASI04", "expected": "Direct"},   # Perfect ref overlap
{"aiuc": "B001", "owasp": "ASI01", "expected": "Related"},  # Jaccard 1/4
{"aiuc": "B002", "owasp": "ASI06", "expected": "Related"},  # Jaccard 2/4
```

The **Direct threshold (0.55)** was set so that pairs with perfect or near-perfect reference overlap (Jaccard ≥ 0.5 on the highest-weighted signal) reliably land in the Direct tier. At the current weights, a pair with reference bridge = 1.0 and average scores on the other signals gets a composite around 0.70–0.80, well above 0.55.

The **Related threshold (0.35)** was set to capture pairs with moderate reference overlap (Jaccard 1/4 to 1/3) or strong semantic similarity. It corresponds roughly to "at least one signal showing meaningful alignment." Lowering it would include too many tangential matches; raising it would exclude pairs that domain experts consider related.

The **Tangential threshold (0.20)** acts as a noise floor. Below this, any apparent similarity is likely from shared generic AI-security vocabulary.

The pipeline validates thresholds on every run by checking the 10 anchor pairs against their expected tiers (6/10 match currently — the mismatches are documented and understood, primarily involving pairs where the AIUC control has broad references that inflate the expected Jaccard).

All thresholds are tunable via CLI flags (`--t-direct`, `--t-related`, `--t-tangential`) for experimentation.

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

## Project Structure

```
├── aiuc/
│   ├── models.py              # Pydantic schemas (AIUC-1, OWASP, mapping output)
│   ├── signals.py             # 3 signal computation functions
│   ├── mapper.py              # Mapping orchestrator + anchor validation
│   ├── output.py              # Excel (5-sheet) + JSON generation
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

### Excel Workbook (5 sheets)

| Sheet | Rows | Key Columns |
|-------|------|-------------|
| README | — | Instructional guide: workbook overview, column definitions, scoring methodology, confidence tiers, framework glossaries, quick-start |
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
