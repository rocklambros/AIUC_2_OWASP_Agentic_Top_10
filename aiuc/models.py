"""Pydantic models for AIUC-1, OWASP Agentic Top 10, and mapping output schemas."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

# ── AIUC-1 Standard Models ──────────────────────────────────────────────────


class ActivityCategory(StrEnum):
    CORE = "Core"
    SUPPLEMENTAL = "Supplemental"


class RationaleCode(StrEnum):
    """Control function class from the rationale taxonomy."""
    PREV = "PREV"
    SCOPE = "SCOPE"
    GATE = "GATE"
    DETECT = "DETECT"
    VALID = "VALID"
    GOVERN = "GOVERN"
    ISOLATE = "ISOLATE"
    DISCLOSE = "DISCLOSE"


class RelevanceLevel(StrEnum):
    """Relevance classification for a control-to-threat mapping."""
    PRIMARY = "Primary"
    SECONDARY = "Secondary"


RATIONALE_LABELS: dict[str, str] = {
    "PREV": "Prevent",
    "SCOPE": "Constrain scope",
    "GATE": "Human gate",
    "DETECT": "Detect and trace",
    "VALID": "Validate and test",
    "GOVERN": "Policy and governance",
    "ISOLATE": "Isolate and contain",
    "DISCLOSE": "Disclose and calibrate",
}


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
    rationale_code: RationaleCode
    rationale_label: str
    relevance: RelevanceLevel
    score: float | None = None
    confidence: ConfidenceTier = ConfidenceTier.NONE
    signals: SignalScores | None = None
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
    rationale_code: RationaleCode
    rationale_label: str
    relevance: RelevanceLevel
    score: float | None = None
    confidence: ConfidenceTier = ConfidenceTier.NONE
    signals: SignalScores | None = None
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
    reference_bridge: float = 0.35
    semantic: float = 0.25
    keyword: float = 0.15
    function_match: float = 0.25


class MappingThresholds(BaseModel):
    direct: float = 0.55
    related: float = 0.28
    tangential: float = 0.20
    governance_floor: float = 0.22


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


# ── V2 Crosswalk Schema Models (standard-agnostic) ─────────────────────────


class StandardInfo(BaseModel):
    """Source or target standard identification."""
    name: str
    version: str
    url: str = ""
    controls: int | None = None
    entries: int | None = None
    domains: int | None = None


class PipelineSignal(BaseModel):
    """A single scoring signal with weight and technique description."""
    weight: float
    technique: str


class PipelineThresholds(BaseModel):
    """Score thresholds for confidence tier classification."""
    direct: float
    related: float
    governance_floor: float | None = None
    tangential: float | None = None


class PipelineConfig(BaseModel):
    """Pipeline signal weights and thresholds."""
    signals: dict[str, PipelineSignal]
    thresholds: PipelineThresholds


class ClassificationAccuracy(BaseModel):
    """Accuracy metrics for a training or validation dataset."""
    standard: str = ""
    mappings: int = 0
    rationale_accuracy: float = 0.0
    relevance_accuracy: float = 0.0


class ClassificationConfig(BaseModel):
    """Rationale taxonomy and relevance configuration."""
    rationale_taxonomy: dict[str, str]
    relevance_levels: list[str]
    classification_accuracy: dict[str, ClassificationAccuracy] = Field(
        default_factory=dict,
    )


class CrosswalkMetadata(BaseModel):
    """Top-level metadata for a v2 crosswalk output."""
    schema_version: str = "2.0"
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    methodology: str = "multi-signal-hybrid-v2"
    source_standard: StandardInfo
    target_standard: StandardInfo
    pipeline: PipelineConfig
    classification: ClassificationConfig


class CrosswalkSummary(BaseModel):
    """Aggregate statistics for the crosswalk output."""
    controls_mapped: str
    controls_unmapped: int
    owasp_entries_with_matches: int
    total_mappings: int
    primary_mappings: int
    secondary_mappings: int
    rationale_distribution: dict[str, int]


class SourceToOwaspMapping(BaseModel):
    """A single source-control-to-OWASP mapping in the v2 schema."""
    owasp_id: str
    owasp_title: str
    relevance: RelevanceLevel
    rationale_code: RationaleCode
    rationale_label: str
    score: float | None = None
    signals: dict[str, float] | None = None


class SourceControlEntry(BaseModel):
    """A source control with its OWASP mappings."""
    control_id: str
    control_title: str
    domain: str
    function_class: RationaleCode
    mapping_count: int
    primary_count: int
    secondary_count: int
    mappings: list[SourceToOwaspMapping] = Field(default_factory=list)


class OwaspToSourceMapping(BaseModel):
    """A single OWASP-to-source-control mapping in the v2 schema."""
    control_id: str
    control_title: str
    domain: str
    function_class: RationaleCode
    relevance: RelevanceLevel
    rationale_code: RationaleCode
    rationale_label: str
    score: float | None = None
    signals: dict[str, float] | None = None


class V2OwaspEntry(BaseModel):
    """An OWASP threat entry with source-control mappings and coverage analysis."""
    owasp_id: str
    owasp_title: str
    owasp_rank: int
    mapping_count: int
    primary_count: int
    secondary_count: int
    function_coverage: dict[str, int] = Field(default_factory=dict)
    uncovered_functions: list[RationaleCode] = Field(default_factory=list)
    mappings: list[OwaspToSourceMapping] = Field(default_factory=list)


class V2ControlLevel(BaseModel):
    """Bi-directional control-level mappings using standard-agnostic field names."""
    source_to_owasp: list[SourceControlEntry] = Field(default_factory=list)
    owasp_to_source: list[V2OwaspEntry] = Field(default_factory=list)


class UnmappedControl(BaseModel):
    """A source control with no OWASP mappings."""
    control_id: str
    control_title: str
    domain: str
    function_class: RationaleCode
    gap_reason: str = ""


class GapAnalysis(BaseModel):
    """Analysis of unmapped controls."""
    unmapped_controls: list[UnmappedControl] = Field(default_factory=list)
    unmapped_count: int = 0
    note: str = ""


class CrosswalkOutput(BaseModel):
    """Top-level v2 crosswalk output conforming to crosswalk-mapping-v2.schema.json."""
    metadata: CrosswalkMetadata
    summary: CrosswalkSummary
    control_level: V2ControlLevel = Field(default_factory=V2ControlLevel)
    gap_analysis: GapAnalysis | None = None


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
