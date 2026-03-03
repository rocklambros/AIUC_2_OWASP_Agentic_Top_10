"""Signal computation for AIUC-1 ↔ OWASP Agentic Top 10 mapping.

Three complementary signals:
  1. Reference Bridge  (weight 0.45) — Jaccard overlap on shared OWASP LLM Top 10 refs
  2. Semantic Similarity (weight 0.35) — Sentence-transformer cosine similarity
  3. TF-IDF Keyword     (weight 0.20) — TF-IDF cosine with synonym expansion
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

    from aiuc.models import Control, OWASPEntry

# ── Synonym groups for domain-specific expansion ────────────────────────────

SYNONYM_GROUPS: list[set[str]] = [
    {"tool call", "tool misuse", "tool invocation", "tool use", "tool execution"},
    {"prompt injection", "adversarial input", "adversarial prompt", "goal hijack"},
    {"privilege", "access control", "authorization", "permission", "least privilege"},
    {"supply chain", "third party", "dependency", "vendor", "third-party"},
    {"code execution", "rce", "remote code execution", "code injection"},
    {"hallucination", "confabulation", "fabricated output", "false output"},
    {"memory", "context", "conversation history", "session state"},
    {"agent communication", "inter-agent", "agent-to-agent", "a2a", "multi-agent"},
    {"cascading failure", "error propagation", "chain failure", "systemic failure"},
    {"trust", "human oversight", "human-in-the-loop", "deception", "social engineering"},
    {"rogue agent", "misalignment", "autonomous misalignment", "uncontrolled agent"},
    {"data privacy", "pii", "personal data", "data leakage", "data protection"},
    {"encryption", "cryptography", "data at rest", "data in transit"},
    {"logging", "audit", "monitoring", "observability", "audit trail"},
    {"identity", "authentication", "credential", "token", "session"},
    {"sandbox", "isolation", "containment", "sandboxing"},
    {"output validation", "output filtering", "output safety", "harmful output"},
    {"input filtering", "input validation", "content filtering"},
    {"adversarial testing", "red team", "penetration testing", "adversarial robustness"},
    {"disclosure", "transparency", "explainability", "labelling"},
    {"incident response", "failure plan", "breach response"},
    {"vendor due diligence", "third-party assessment", "supply chain risk"},
    {"acceptable use", "usage policy", "terms of use"},
    {"ip protection", "intellectual property", "trade secret", "copyright"},
    {"regulatory compliance", "gdpr", "eu ai act", "regulation"},
]


def _normalize_llm_ref(ref: str) -> str:
    """Normalize LLM references like 'LLM01:2025' → 'LLM01'."""
    match = re.match(r"(LLM\d{2})", ref)
    return match.group(1) if match else ref


# ── Signal 1: Reference Bridge ──────────────────────────────────────────────


def _extract_llm_refs_from_text(text: str) -> set[str]:
    """Extract OWASP LLM Top 10 references from text."""
    raw = re.findall(r"LLM\d{2}(?::\d{4})?", text)
    return {_normalize_llm_ref(r) for r in raw}


def extract_aiuc_llm_refs(control: Control) -> set[str]:
    """Extract LLM refs from an AIUC-1 control's framework_references + description."""
    refs: set[str] = set()
    for raw in control.framework_references.owasp_llm_top10:
        refs.add(_normalize_llm_ref(raw))
    refs |= _extract_llm_refs_from_text(control.description)
    return refs


def extract_owasp_llm_refs(entry: OWASPEntry) -> set[str]:
    """Extract LLM refs from an OWASP Agentic entry."""
    all_text = entry.description + " " + " ".join(entry.prevention_guidelines)
    return _extract_llm_refs_from_text(all_text)


def compute_reference_bridge(
    aiuc_controls: list[Control],
    owasp_entries: list[OWASPEntry],
) -> NDArray[np.float64]:
    """Compute Jaccard similarity on shared OWASP LLM Top 10 references.

    Returns matrix of shape (len(aiuc_controls), len(owasp_entries)).
    """
    aiuc_refs = [extract_aiuc_llm_refs(c) for c in aiuc_controls]
    owasp_refs = [extract_owasp_llm_refs(e) for e in owasp_entries]

    n_aiuc = len(aiuc_controls)
    n_owasp = len(owasp_entries)
    matrix = np.zeros((n_aiuc, n_owasp), dtype=np.float64)

    for i in range(n_aiuc):
        for j in range(n_owasp):
            a, b = aiuc_refs[i], owasp_refs[j]
            if not a and not b:
                continue
            intersection = len(a & b)
            union = len(a | b)
            matrix[i, j] = intersection / union if union > 0 else 0.0

    return matrix


# ── Signal 2: Semantic Similarity ────────────────────────────────────────────


def _build_document_text(control: Control) -> str:
    """Build a rich text representation of an AIUC control for embedding."""
    parts = [control.title, control.description]
    for act in control.activities:
        parts.append(act.description)
    parts.extend(control.keywords)
    return " ".join(p for p in parts if p)


def _build_owasp_text(entry: OWASPEntry) -> str:
    """Build a rich text representation of an OWASP entry for embedding."""
    parts = [entry.title, entry.description]
    parts.extend(entry.prevention_guidelines)
    parts.extend(entry.common_examples)
    return " ".join(p for p in parts if p)


def compute_semantic_similarity(
    aiuc_controls: list[Control],
    owasp_entries: list[OWASPEntry],
    model_name: str = "all-MiniLM-L6-v2",
) -> NDArray[np.float64]:
    """Compute cosine similarity using sentence-transformer embeddings.

    Returns matrix of shape (len(aiuc_controls), len(owasp_entries)).
    Z-score normalized within each AIUC control row to discriminate
    beyond the high baseline similarity that all AI-security texts share.
    """
    from sentence_transformers import SentenceTransformer

    model: SentenceTransformer = SentenceTransformer(model_name)

    aiuc_texts = [_build_document_text(c) for c in aiuc_controls]
    owasp_texts = [_build_owasp_text(e) for e in owasp_entries]

    aiuc_embeddings = model.encode(aiuc_texts, show_progress_bar=False)
    owasp_embeddings = model.encode(owasp_texts, show_progress_bar=False)

    raw_sim: NDArray[np.float64] = sklearn_cosine(aiuc_embeddings, owasp_embeddings)

    # Z-score normalize per row (per AIUC control)
    row_means = raw_sim.mean(axis=1, keepdims=True)
    row_stds = raw_sim.std(axis=1, keepdims=True)
    row_stds = np.where(row_stds < 1e-8, 1.0, row_stds)
    z_scores = (raw_sim - row_means) / row_stds

    # Scale z-scores to [0, 1] range using sigmoid-like transform
    normalized = 1.0 / (1.0 + np.exp(-z_scores))

    result: NDArray[np.float64] = normalized.astype(np.float64)
    return result


# ── Signal 3: TF-IDF Keyword Overlap ────────────────────────────────────────


def _expand_synonyms(text: str) -> str:
    """Expand text with synonyms from domain-specific groups."""
    text_lower = text.lower()
    expansions: list[str] = []
    for group in SYNONYM_GROUPS:
        matched = [term for term in group if term in text_lower]
        if matched:
            expansions.extend(group - set(matched))
    return text + " " + " ".join(expansions)


def compute_keyword_similarity(
    aiuc_controls: list[Control],
    owasp_entries: list[OWASPEntry],
) -> NDArray[np.float64]:
    """Compute TF-IDF cosine similarity with synonym expansion.

    Returns matrix of shape (len(aiuc_controls), len(owasp_entries)).
    """
    aiuc_texts = [_expand_synonyms(_build_document_text(c)) for c in aiuc_controls]
    owasp_texts = [_expand_synonyms(_build_owasp_text(e)) for e in owasp_entries]

    all_texts = aiuc_texts + owasp_texts
    n_aiuc = len(aiuc_texts)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words="english",
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    aiuc_vectors = tfidf_matrix[:n_aiuc]
    owasp_vectors = tfidf_matrix[n_aiuc:]

    similarity: NDArray[np.float64] = sklearn_cosine(aiuc_vectors, owasp_vectors)
    return similarity.astype(np.float64)


# ── Composite Score ──────────────────────────────────────────────────────────


def compute_composite_scores(
    aiuc_controls: list[Control],
    owasp_entries: list[OWASPEntry],
    weights: tuple[float, float, float] = (0.45, 0.35, 0.20),
    model_name: str = "all-MiniLM-L6-v2",
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Compute all three signals and the weighted composite.

    Args:
        aiuc_controls: List of AIUC-1 controls.
        owasp_entries: List of OWASP Agentic Top 10 entries.
        weights: Tuple of (reference_bridge, semantic, keyword) weights.
        model_name: Sentence transformer model name.

    Returns:
        Tuple of (composite, reference_bridge, semantic, keyword) matrices.
        Each has shape (len(aiuc_controls), len(owasp_entries)).
    """
    w_ref, w_sem, w_kw = weights

    ref_bridge = compute_reference_bridge(aiuc_controls, owasp_entries)
    semantic = compute_semantic_similarity(aiuc_controls, owasp_entries, model_name)
    keyword = compute_keyword_similarity(aiuc_controls, owasp_entries)

    composite = w_ref * ref_bridge + w_sem * semantic + w_kw * keyword

    return composite, ref_bridge, semantic, keyword
