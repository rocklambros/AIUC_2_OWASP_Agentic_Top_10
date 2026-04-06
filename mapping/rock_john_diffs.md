# AIUC-1 / OWASP Agentic Top 10 Mapping Differences

**Comparing:** John Sotiropoulos crosswalk (March 15, 2026) vs. Rock/Lambros automated mapping (March 3, 2026)

---

## 1. Methodology Differences

| Dimension | Rock/Lambros (JSON/Excel) | John (Crosswalk) |
|-----------|--------------------------|-------------------|
| **Approach** | Algorithmic multi-signal hybrid (reference bridge, semantic similarity, keyword overlap) | Expert manual review with domain judgment |
| **Scoring** | Composite 0.0-1.0 with weighted sub-scores (ref=0.45, semantic=0.35, keyword=0.20) | No numeric scores |
| **Confidence tiers** | Direct (>0.55), Related (>0.35); below 0.35 excluded | Primary (directly mitigates core risk), Secondary (related consequence or supporting control) |
| **Granularity** | Control-level + sub-activity-level (190 activity rows) | Control-level only |
| **Total control-level mappings** | 38 unique AIUC-OWASP pairs | 79 unique AIUC-OWASP pairs (59 Primary, 20 Secondary) |
| **AIUC controls mapped** | 19 of 41 controls have at least one mapping | 28 of 41 controls have at least one mapping |
| **Relationship types** | Labeled as "Prevents" or "Detects" | No relationship-type labels |
| **Gap analysis** | None documented | Two explicit gaps identified (inter-agent auth, agent attestation) |
| **OWASP companion refs** | None | Extensive "See also" references to 7 OWASP publications |

---

## 2. Coverage Summary

### Controls with mappings in each source

| Source | Mapped controls | Unmapped controls |
|--------|----------------|-------------------|
| Rock/Lambros | A003, A004, A007, B001-B005, B007, B009, C003-C006, D001-D004, E005, E006, E009 (19) | 22 controls |
| John | A003-A005, A007, B001-B002, B005-B009, C003-C004, C006-C009, D001-D004, E001-E003, E005-E006, E009, E015-E016 (28) | 13 controls |

### OWASP threat coverage (number of AIUC controls mapped)

| OWASP Threat | Rock/Lambros | John | Delta |
|-------------|-------------|------|-------|
| ASI01 Agent Goal Hijack | 3 | 9 | **+6** |
| ASI02 Tool Misuse | 4 | 7 | **+3** |
| ASI03 Identity & Privilege Abuse | 1 | 7 | **+6** |
| ASI04 Supply Chain | 5 | 6 | **+1** |
| ASI05 Unexpected Code Execution | 7 | 8 | **+1** |
| ASI06 Memory & Context Poisoning | 3 | 9 | **+6** |
| ASI07 Insecure Inter-Agent Comms | **0** | **5** | **+5** |
| ASI08 Cascading Failures | 1 | 10 | **+9** |
| ASI09 Human-Agent Trust | 8 | 8 | 0 |
| ASI10 Rogue Agents | 4 | 10 | **+6** |

---

## 3. Per-AIUC-Control Mapping Differences

Below, each control that differs between sources is listed. "RL" = Rock/Lambros, "JS" = John Sotiropoulos.

### A. Data & Privacy

#### A003 - Limit AI agent data collection

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI02 | Related | Primary | **Agreement** (both map, JS upgrades to Primary) |
| ASI06 | -- | Primary | **JS adds** |
| ASI09 | Related | -- | **RL adds** (score 0.363) |

#### A004 - Protect IP & trade secrets

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI04 | Related | Primary | **Agreement** (JS upgrades) |

#### A005 - Prevent cross-customer data exposure

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI06 | -- | Primary | **JS adds** (RL had no mapping for A005) |

#### A007 - Prevent IP violations

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI04 | Related | Primary | **Agreement** (JS upgrades) |

### B. Security

#### B001 - Third-party testing of adversarial robustness

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | Related (0.357) | Primary | **Agreement** (JS upgrades) |
| ASI05 | Related (0.521) | Secondary | **Agreement** (different tier labels) |
| ASI06 | Related (0.519) | Primary | **Agreement** (JS upgrades) |
| ASI10 | -- | Secondary | **JS adds** |

#### B002 - Detect adversarial input

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | Related (0.453) | Primary | **Agreement** (JS upgrades) |
| ASI05 | Related (0.432) | -- | **RL adds** |
| ASI06 | Related (0.443) | Primary | **Agreement** (JS upgrades) |

#### B003 - Manage public release of technical details

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI10 | Related (0.389) | -- | **RL maps, JS does not map B003 at all** |

#### B004 - Prevent AI endpoint scraping

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI09 | Related (0.365) | -- | **RL maps, JS does not map B004 at all** |

#### B005 - Implement real-time input filtering

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | Related (0.420) | Primary | **Agreement** (JS upgrades) |
| ASI05 | Related (0.431) | Secondary | **Agreement** (different tier labels) |
| ASI06 | Related (0.417) | Secondary | **Agreement** |
| ASI08 | Related (0.369) | -- | **RL adds** |

#### B006 - Prevent unauthorized AI agent actions

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Primary | **JS adds** |
| ASI02 | -- | Primary | **JS adds** |
| ASI03 | -- | Primary | **JS adds** |
| ASI05 | -- | Primary | **JS adds** |
| ASI06 | -- | Primary | **JS adds** |
| ASI07 | -- | Primary | **JS adds** |
| ASI08 | -- | Primary | **JS adds** |
| ASI10 | -- | Primary | **JS adds** |

> **Major divergence.** RL produced zero mappings for B006 despite it being a central agentic security control. JS maps it to 8 of 10 threats, all Primary. This is the single largest gap in the automated approach.

#### B007 - Enforce user access privileges to AI systems

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI02 | Related (0.399) | Primary | **Agreement** (JS upgrades) |
| ASI03 | Related (0.484) | Primary | **Agreement** (JS upgrades) |
| ASI07 | -- | Primary | **JS adds** |
| ASI09 | Related (0.362) | -- | **RL adds** |
| ASI10 | Related (0.413) | Primary | **Agreement** (JS upgrades) |

#### B008 - Protect model deployment environment

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI03 | -- | Primary | **JS adds** |
| ASI04 | -- | Primary | **JS adds** |
| ASI05 | -- | Primary | **JS adds** |
| ASI07 | -- | Primary | **JS adds** |
| ASI10 | -- | Primary | **JS adds** |

> **Major divergence.** RL produced zero mappings for B008. JS maps it to 5 threats, all Primary.

#### B009 - Limit output over-exposure

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI05 | Related (0.380) | -- | **RL adds** |
| ASI06 | -- | Secondary | **JS adds** |
| ASI09 | -- | Secondary | **JS adds** |
| ASI10 | Related (0.396) | -- | **RL adds** |

> **Full disagreement.** Zero overlap between the two mappings.

### C. Safety

#### C003 - Prevent harmful outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Secondary | **JS adds** |
| ASI08 | -- | Secondary | **JS adds** |
| ASI09 | Direct (0.558) | Secondary | **Agreement** (RL rates higher, JS rates Secondary) |

#### C004 - Prevent out-of-scope outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Secondary | **JS adds** |
| ASI05 | Related (0.458) | -- | **RL adds** |

> **Full disagreement.** Zero overlap.

#### C005 - Prevent customer-defined high risk outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI05 | Related (0.371) | -- | **RL maps, JS does not map C005 at all** |
| ASI09 | Related (0.397) | -- | **RL maps, JS does not map C005 at all** |

#### C006 - Prevent output vulnerabilities

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Secondary | **JS adds** |
| ASI05 | Direct (0.570) | Primary | **Agreement** |

#### C007 - Flag high risk outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Secondary | **JS adds** |
| ASI09 | -- | Primary | **JS adds** |
| ASI10 | -- | Secondary | **JS adds** |

> RL produced no mapping for C007; JS maps it to 3 threats.

#### C008 - Monitor AI risk categories

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI10 | -- | Secondary | **JS adds** (RL had no mapping) |

#### C009 - Enable real-time feedback and intervention

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI09 | -- | Primary | **JS adds** (RL had no mapping) |

### D. Reliability

#### D001 - Prevent hallucinated outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Primary | **JS adds** |
| ASI09 | Related (0.500) | Primary | **Agreement** (JS upgrades) |

#### D002 - Third-party testing for hallucinations

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Primary | **JS adds** |
| ASI09 | Related (0.428) | Primary | **Agreement** (JS upgrades) |
| ASI10 | Related (0.362) | -- | **RL adds** |

#### D003 - Restrict unsafe tool calls

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Primary | **JS adds** |
| ASI02 | Related (0.497) | Primary | **Agreement** (JS upgrades) |
| ASI03 | -- | Secondary | **JS adds** |
| ASI05 | -- | Primary | **JS adds** |
| ASI06 | -- | Secondary | **JS adds** |
| ASI08 | -- | Primary | **JS adds** |
| ASI10 | -- | Primary | **JS adds** |

> **Major divergence.** RL maps D003 to only ASI02. JS maps it to 7 threats (5 Primary, 2 Secondary).

#### D004 - Third-party testing of tool calls

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI02 | Direct (0.779) | Primary | **Agreement** |
| ASI03 | -- | Secondary | **JS adds** |
| ASI05 | -- | Primary | **JS adds** |
| ASI10 | -- | Primary | **JS adds** |

### E. Accountability

#### E001 - AI failure plan for security breaches

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Primary | **JS adds** (RL had no mapping) |
| ASI10 | -- | Primary | **JS adds** |

#### E002 - AI failure plan for harmful outputs

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Primary | **JS adds** (RL had no mapping) |

#### E003 - AI failure plan for hallucinations

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI08 | -- | Primary | **JS adds** (RL had no mapping) |

#### E005 - Assess cloud vs on-prem processing

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI04 | Direct (0.661) | Secondary | **Disagreement on tier** (RL rates Direct/high-score, JS rates Secondary) |

#### E006 - Conduct vendor due diligence

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI04 | Direct (0.752) | Primary | **Agreement** |

#### E009 - Monitor third-party access

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI02 | -- | Primary | **JS adds** |
| ASI03 | -- | Primary | **JS adds** |
| ASI04 | Related (0.358) | Primary | **Agreement** (JS upgrades) |
| ASI07 | -- | Primary | **JS adds** |
| ASI09 | Related (0.386) | -- | **RL adds** |

#### E015 - Log model activity

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI01 | -- | Primary | **JS adds** |
| ASI02 | -- | Secondary | **JS adds** |
| ASI03 | -- | Primary | **JS adds** |
| ASI05 | -- | Secondary | **JS adds** |
| ASI06 | -- | Primary | **JS adds** |
| ASI07 | -- | Primary | **JS adds** |
| ASI08 | -- | Primary | **JS adds** |
| ASI09 | -- | Primary | **JS adds** |
| ASI10 | -- | Primary | **JS adds** |

> **Most extreme divergence.** RL produced zero mappings for E015. JS maps it to all 10 OWASP threats (7 Primary, 2 Secondary), noting it as the most broadly mapped requirement. This reflects a fundamental limitation of the automated approach: logging/auditing is semantically distant from specific attack descriptions despite being universally relevant as a detective control.

#### E016 - Implement AI disclosure mechanisms

| OWASP | RL | JS | Difference |
|-------|----|----|------------|
| ASI09 | -- | Primary | **JS adds** (RL had no mapping) |

---

## 4. Per-OWASP-Threat Differences (Reverse View)

### ASI07 - Insecure Inter-Agent Communication

| AIUC | RL | JS |
|------|----|----|
| B006 | -- | Primary |
| B007 | -- | Primary |
| B008 | -- | Primary |
| E009 | -- | Primary |
| E015 | -- | Primary |

> RL identified this as a **complete gap** (zero mappings). JS maps 5 controls, all Primary.

### ASI08 - Cascading Failures

| AIUC | RL | JS |
|------|----|----|
| B005 | Related (0.369) | -- |
| B006 | -- | Primary |
| C003 | -- | Secondary |
| C007 | -- | Secondary |
| D001 | -- | Primary |
| D002 | -- | Primary |
| D003 | -- | Primary |
| E001 | -- | Primary |
| E002 | -- | Primary |
| E003 | -- | Primary |
| E015 | -- | Primary |

> RL had only 1 mapping; JS has 10 (7 Primary, 2 Secondary). The single RL mapping (B005) is not in JS. Zero overlap.

---

## 5. Mappings Unique to Rock/Lambros (Not in John)

These 11 AIUC-OWASP pairs appear only in the automated mapping:

| AIUC | OWASP | RL Score | Notes |
|------|-------|----------|-------|
| A003 | ASI09 | 0.363 | High semantic (0.782) but low ref bridge (0.167) |
| B002 | ASI05 | 0.432 | High semantic (0.844) drove inclusion |
| B003 | ASI10 | 0.389 | JS excludes B003 entirely |
| B004 | ASI09 | 0.365 | JS excludes B004 entirely |
| B005 | ASI08 | 0.369 | Only RL mapping for ASI08 |
| B007 | ASI09 | 0.362 | Borderline score |
| B009 | ASI05 | 0.380 | JS maps B009 to ASI06/ASI09 instead |
| B009 | ASI10 | 0.396 | JS maps B009 to ASI06/ASI09 instead |
| C004 | ASI05 | 0.458 | JS maps C004 to ASI01 instead |
| C005 | ASI05 | 0.371 | JS excludes C005 entirely |
| C005 | ASI09 | 0.397 | JS excludes C005 entirely |
| D002 | ASI10 | 0.362 | Borderline score |
| E009 | ASI09 | 0.386 | JS maps E009 to ASI02/03/04/07 instead |

---

## 6. Controls Mapped by John but Entirely Absent in Rock/Lambros

These 9 AIUC controls have zero mappings in RL but one or more in JS:

| AIUC | JS Maps To | JS Total Mappings |
|------|-----------|-------------------|
| **B006** | ASI01, ASI02, ASI03, ASI05, ASI06, ASI07, ASI08, ASI10 | **8** (all Primary) |
| **B008** | ASI03, ASI04, ASI05, ASI07, ASI10 | **5** (all Primary) |
| **E015** | ASI01-ASI10 (all) | **9** (7P + 2S) |
| **E016** | ASI09 | **1** (Primary) |
| **C007** | ASI08, ASI09, ASI10 | **3** (1P + 2S) |
| **C008** | ASI10 | **1** (Secondary) |
| **C009** | ASI09 | **1** (Primary) |
| **E001** | ASI08, ASI10 | **2** (both Primary) |
| **E002** | ASI08 | **1** (Primary) |
| **E003** | ASI08 | **1** (Primary) |
| **A005** | ASI06 | **1** (Primary) |

---

## 7. Tier/Relevance Disagreements on Shared Mappings

Where both sources map the same AIUC-OWASP pair but assign different importance:

| AIUC | OWASP | RL Tier | JS Tier | Assessment |
|------|-------|---------|---------|------------|
| C003 | ASI09 | Direct (0.558) | Secondary | **RL rates higher** than JS |
| E005 | ASI04 | Direct (0.661) | Secondary | **RL rates higher** than JS |
| B001 | ASI05 | Related (0.521) | Secondary | Comparable |
| B005 | ASI05 | Related (0.431) | Secondary | Comparable |

> In most shared mappings, JS assigns a higher tier (Primary) to pairs that RL scored as "Related." However, for C003→ASI09 and E005→ASI04, the direction reverses: RL's algorithm scored these as Direct while JS rated them only Secondary.

---

## 8. Structural Differences

### John includes but Rock/Lambros does not

1. **OWASP descriptions** - Full threat descriptions with real-world examples (EchoLeak, Amazon Q, AutoGPT RCE, Gemini Memory Attack, Replit meltdown)
2. **"See also" references** - Cross-references to 7 OWASP companion publications per threat
3. **Gap analysis** - Two explicit AIUC-1 gaps identified:
   - Inter-agent communication security (ASI07, ASI10)
   - Agent identity attestation and containment (ASI10, ASI03)
4. **Contributor guidance** - Notes for reviewers with 5 action items
5. **Unmapped requirements table** - Explicit list of 19 controls not mapped with principle labels

### Rock/Lambros includes but John does not

1. **Numeric scores** - Composite scores and 3 sub-signal breakdowns per mapping
2. **Sub-activity-level mappings** - 190 granular activity-to-threat mappings
3. **Relationship types** - "Prevents" vs "Detects" classification
4. **Confidence thresholds** - Documented scoring methodology with explicit cutoffs

---

## 9. Root Cause Analysis of Divergences

### Why RL missed B006, B008, E015, and the E-domain failure plans

The automated approach relies on textual similarity (semantic embeddings + keyword overlap + reference bridges). Controls like B006 ("Prevent unauthorized AI agent actions") are **broad preventive controls** whose text does not closely match any single OWASP threat description. Similarly, E015 ("Log model activity") is a **horizontal detective control** relevant to all threats but textually similar to none. The algorithm's threshold-based filtering removes these low-score but high-relevance mappings.

### Why RL found mappings JS excluded (B003, B004, C005)

The semantic similarity component sometimes surfaces pairs with high text similarity but low domain relevance. For example, B004 ("Prevent AI endpoint scraping") scores high semantic similarity with ASI09 (trust exploitation) due to shared attack-surface language, but JS correctly judges the controls address different risk domains.

### Why ASI08 (Cascading Failures) is nearly empty in RL

Cascading failures is an emergent systems-level risk. Its OWASP description focuses on error propagation and self-reinforcement - concepts that are architecturally relevant but textually distant from individual AIUC control descriptions. JS correctly identifies that failure plans (E001-E003), hallucination controls (D001-D002), and tool restrictions (D003) all mitigate cascading risk through different mechanisms.

---

## 10. Summary Statistics

| Metric | Rock/Lambros | John | Overlap |
|--------|-------------|------|---------|
| Total AIUC-OWASP pairs | 38 | 79 | 26 shared pairs |
| Unique to source | 12 | 53 | -- |
| Controls mapped | 19 | 28 | 17 shared controls |
| OWASP threats fully covered | 9 of 10 | 10 of 10 | -- |
| ASI07 mappings | 0 | 5 | -- |
| ASI08 mappings | 1 | 10 | 0 shared |
| Controls with 0 mappings | 22 | 13 | -- |

---

## 11. Recommendations for Reconciliation

1. **B006, B008, E015** - Accept JS mappings. These are foundational agentic security controls that the automated approach structurally cannot score well due to their broad applicability.

2. **ASI07 and ASI08** - Accept JS mappings. Both threats require domain expertise to map; automated semantic similarity fails on emergent/systemic risks.

3. **E001-E003 (failure plans)** - Accept JS mappings to ASI08. Incident response plans directly mitigate cascading failure impact.

4. **B003→ASI10, B004→ASI09** - Review RL-unique mappings. These are borderline and may be semantic false positives. JS's exclusion appears well-reasoned.

5. **C003→ASI09 and E005→ASI04 tier disagreement** - Discuss. RL's high scores suggest strong textual alignment; JS's Secondary rating suggests the expert sees these as indirect. Both positions are defensible.

6. **C005 mappings** - Discuss whether JS should include C005. RL found Related-level connections to ASI05 and ASI09 that may have been overlooked.

7. **Gap analysis** - Adopt JS's two identified AIUC-1 gaps (inter-agent auth, agent attestation) as formal recommendations. The automated approach independently confirmed ASI07 as a blind spot.

8. **Scoring calibration** - Consider lowering RL thresholds for broad preventive/detective controls, or adding a manual "cross-cutting control" flag to override threshold filtering for controls like B006, E015, and E001-E003.
