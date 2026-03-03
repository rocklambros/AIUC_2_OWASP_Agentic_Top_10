"""Pydantic models for AIUC-1, OWASP Agentic Top 10, and mapping output schemas."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

# ── AIUC-1 Standard Models ──────────────────────────────────────────────────


class ActivityCategory(StrEnum):
    CORE = "Core"
    SUPPLEMENTAL = "Supplemental"


class Activity(BaseModel):
    id: str
    description: str
    category: ActivityCategory = ActivityCategory.CORE
    evidence_types: list[str] = Field(default_factory=list)


class FrameworkReferences(BaseModel):
    eu_ai_act: list[str] = Field(default_factory=list)
    iso_42001: list[str] = Field(default_factory=list)
    nist_ai_rmf: list[str] = Field(default_factory=list)
    csa_aicm: list[str] = Field(default_factory=list)
    owasp_llm_top10: list[str] = Field(default_factory=list)
    owasp_aivss: list[str] = Field(default_factory=list)
    mitre_atlas: list[str] = Field(default_factory=list)


class Control(BaseModel):
    id: str
    title: str
    url: str = ""
    classification: str = ""
    type: str = ""
    frequency: str = ""
    description: str = ""
    applicable_capabilities: list[str] = Field(default_factory=list)
    activities: list[Activity] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    framework_references: FrameworkReferences = Field(default_factory=FrameworkReferences)


class Domain(BaseModel):
    id: str
    name: str
    url: str = ""
    description: str = ""
    controls: list[Control] = Field(default_factory=list)


class AIUC1Standard(BaseModel):
    standard: str = "AIUC-1"
    version: str = "1.0"
    url: str = "https://www.aiuc-1.com"
    scraped_at: str = ""
    domains: list[Domain] = Field(default_factory=list)


# ── OWASP Agentic Top 10 Models ─────────────────────────────────────────────


class OWASPEntry(BaseModel):
    rank: int
    identifier: str
    title: str
    description: str = ""
    common_examples: list[str] = Field(default_factory=list)
    attack_scenarios: list[str] = Field(default_factory=list)
    prevention_guidelines: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)


class OWASPAgenticTop10(BaseModel):
    title: str = "OWASP Top 10 for Agentic Applications"
    version: str = "2026"
    entries: list[OWASPEntry] = Field(default_factory=list)


# ── Mapping Output Models ────────────────────────────────────────────────────


class ConfidenceTier(StrEnum):
    DIRECT = "Direct"
    RELATED = "Related"
    TANGENTIAL = "Tangential"
    NONE = "None"


class RelationshipType(StrEnum):
    MITIGATES = "Mitigates"
    DETECTS = "Detects"
    PREVENTS = "Prevents"
    ADDRESSES = "Addresses"
    PARTIALLY_ADDRESSES = "Partially Addresses"


class SignalScores(BaseModel):
    reference_bridge: float = 0.0
    semantic: float = 0.0
    keyword: float = 0.0


class ControlMapping(BaseModel):
    owasp_id: str
    owasp_title: str
    score: float
    confidence: ConfidenceTier
    signals: SignalScores
    relationship_type: RelationshipType = RelationshipType.ADDRESSES


class AIUCToOWASPControl(BaseModel):
    aiuc_id: str
    aiuc_title: str
    aiuc_domain: str
    mappings: list[ControlMapping] = Field(default_factory=list)


class OWASPControlMapping(BaseModel):
    aiuc_id: str
    aiuc_title: str
    aiuc_domain: str
    score: float
    confidence: ConfidenceTier
    signals: SignalScores
    relationship_type: RelationshipType = RelationshipType.ADDRESSES


class OWASPToAIUCControl(BaseModel):
    owasp_id: str
    owasp_title: str
    owasp_rank: int
    mappings: list[OWASPControlMapping] = Field(default_factory=list)


class SubActivityMapping(BaseModel):
    owasp_id: str
    score: float
    confidence: ConfidenceTier


class AIUCToOWASPSubActivity(BaseModel):
    activity_id: str
    parent_control: str
    description: str
    mappings: list[SubActivityMapping] = Field(default_factory=list)


class OWASPSubActivityMapping(BaseModel):
    activity_id: str
    parent_control: str
    score: float
    confidence: ConfidenceTier


class OWASPToAIUCSubActivity(BaseModel):
    owasp_id: str
    owasp_title: str
    mappings: list[OWASPSubActivityMapping] = Field(default_factory=list)


class MappingWeights(BaseModel):
    reference_bridge: float = 0.45
    semantic: float = 0.35
    keyword: float = 0.20


class MappingThresholds(BaseModel):
    direct: float = 0.55
    related: float = 0.35
    tangential: float = 0.20


class MappingMetadata(BaseModel):
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    methodology: str = "multi-signal-hybrid"
    version: str = "1.0"
    weights: MappingWeights = Field(default_factory=MappingWeights)
    thresholds: MappingThresholds = Field(default_factory=MappingThresholds)


class ControlLevelMappings(BaseModel):
    aiuc_to_owasp: list[AIUCToOWASPControl] = Field(default_factory=list)
    owasp_to_aiuc: list[OWASPToAIUCControl] = Field(default_factory=list)


class SubActivityLevelMappings(BaseModel):
    aiuc_to_owasp: list[AIUCToOWASPSubActivity] = Field(default_factory=list)
    owasp_to_aiuc: list[OWASPToAIUCSubActivity] = Field(default_factory=list)


class MappingOutput(BaseModel):
    metadata: MappingMetadata = Field(default_factory=MappingMetadata)
    control_level: ControlLevelMappings = Field(default_factory=ControlLevelMappings)
    sub_activity_level: SubActivityLevelMappings = Field(default_factory=SubActivityLevelMappings)


# ── Helper for confidence tier classification ────────────────────────────────


def classify_confidence(
    score: float,
    thresholds: MappingThresholds | None = None,
) -> ConfidenceTier:
    """Classify a composite score into a confidence tier."""
    t = thresholds or MappingThresholds()
    if score >= t.direct:
        return ConfidenceTier.DIRECT
    if score >= t.related:
        return ConfidenceTier.RELATED
    if score >= t.tangential:
        return ConfidenceTier.TANGENTIAL
    return ConfidenceTier.NONE


def infer_relationship_type(
    signals: SignalScores,
    aiuc_control: Control | None = None,
) -> RelationshipType:
    """Infer the relationship type based on signal distribution and control metadata."""
    if aiuc_control:
        ctrl_type = aiuc_control.type.lower()
        if "preventative" in ctrl_type or "preventive" in ctrl_type:
            return RelationshipType.PREVENTS
        if "detective" in ctrl_type:
            return RelationshipType.DETECTS

    if signals.reference_bridge > 0.6:
        return RelationshipType.MITIGATES
    if signals.semantic > 0.6:
        return RelationshipType.ADDRESSES
    return RelationshipType.PARTIALLY_ADDRESSES
