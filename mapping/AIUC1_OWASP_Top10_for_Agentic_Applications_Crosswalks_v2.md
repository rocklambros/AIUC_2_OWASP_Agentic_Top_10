# AIUC-1 \- OWASP Top10 for Agentic Applications \- Crosswalks.

**DRAFT**

**Document log**

| Date | Author | Contribution |
| :---- | :---- | :---- |
| **March 15, 2026** | **John Sotiropoulos** | **Initial Draft** |
| **March 16, 2026** | **Rock Lambros** | **Merged automated mapping; independent review pass; expanded gap analysis** |
|  |  |  |
|  |  |  |

# **Introduction**

This document provides a bidirectional crosswalk between **AIUC-1** and the **OWASP Top 10 for Agentic Applications (2026)**.

The OWASP Top 10 for Agentic Applications is a globally peer-reviewed framework identifying the most critical security risks facing autonomous and agentic AI systems. Published in December 2025 by the OWASP GenAI Security Project's Agentic Security Initiative, it provides actionable guidance for securing AI agents that plan, act, and make decisions across complex workflows.

AIUC-1 is a security, safety, and reliability standard for AI agents, organized across six principles: Data & Privacy, Security, Safety, Reliability, Accountability, and Society. This crosswalk proposes mappings between the two frameworks to help practitioners working with either standard understand how they relate.

The document is organized in two parts:

* **Part A \- AIUC-1 Requirements** \-\> **OWASP Agentic Top 10\.** For each AIUC-1 requirement that maps to the Agentic Top 10, this section shows which threats it addresses. This view helps organizations already working with AIUC-1 understand their coverage of agentic risks.
* **Part B \- OWASP Agentic Top 10 \-\> AIUC-1 Requirements.** For each of the 10 OWASP Agentic Top 10, this section shows which AIUC-1 requirements are relevant. This view helps practitioners using the OWASP Top 10 refer back to AIUC-1 controls and requirements.

Each mapping is labeled **Primary** (directly mitigates the core risk) or **Secondary** (addresses a related consequence or supporting control). Both parts are generated from the same underlying mapping data.

### **Methodology note**

This crosswalk combines expert domain review with automated multi-signal analysis (reference-bridge, semantic similarity, and keyword signals). Mappings originating from the expert review carry no provenance marker. Mappings surfaced by the automated analysis are marked **\[A\]**. Mappings added during a subsequent review against OWASP prevention guidelines are marked **\[R\]**. The team should validate all marked mappings and upgrade, retain, or remove them as appropriate.

### **Related OWASP Agentic Security Initiative publications**

The OWASP Top 10 for Agentic Applications is part of a broader suite of resources from the OWASP GenAI Security Project's Agentic Security Initiative (genai.owasp.org). These companion documents provide deeper technical context for the threats and mitigations referenced in this crosswalk:

* **Agentic AI \- Threats and Mitigations v1.1** (February 2025; updated December 2025\) \- The foundational threat taxonomy underpinning the Top 10\. Provides detailed threat models, attack trees, and mitigation strategies for each risk category.
* **Multi-Agentic System Threat Modeling Guide v1.0** (April 2025\) \- Threat modeling guidance specific to multi-agent architectures. Particularly relevant to ASI07 and ASI10.
* **Agent Name Service (ANS) for Secure AI Agent Discovery v1.0** (May 2025\) \- A DNS-inspired framework for agent identity and discovery using PKI. Relevant to the AIUC-1 gaps identified under ASI07 and ASI10.
* **Securing Agentic Applications Guide 1.0** (July 2025\) \- Practical technical guidance for securely designing and deploying LLM-powered agentic applications.
* **State of Agentic AI Security and Governance 1.0** (August 2025\) \- A governance-focused guide covering frameworks, regulatory standards, and organizational practices for responsible agentic AI deployment.
* **CheatSheet \- A Practical Guide for Securely Using Third-Party MCP Servers 1.0** (November 2025\) \- Focused guidance on securing Model Context Protocol (MCP) server integrations. Particularly relevant to ASI04 and ASI02.
* **A Practical Guide for Secure MCP Server Development** (February 2026\) \- Developer-focused guidance for building secure MCP servers. Relevant to ASI04 and ASI05.

# **Part A \- AIUC-1 Requirements \-\> OWASP Agentic Top 10**

This section starts from each AIUC-1 requirement and shows which OWASP Agentic Top 10 threats it addresses. The crosswalk allows AIUC-1 practitioners to find and use the appropriate OWASP Agentic Top 10 items and understand the relevant threat and mitigations. Only requirements with at least one mapping are listed. Requirements with no mapping to the OWASP Top 10 for Agentic Applications are listed at the end of this section.

## **A. Data & Privacy**

### **A003 \- Limit AI agent data collection**

Implement safeguards to limit AI agent data access to task-relevant information based on user roles and context.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[A\] |

### **A004 \- Protect IP & trade secrets**

Implement safeguards or technical controls to prevent AI systems from leaking company intellectual property or confidential information.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |

### **A005 \- Prevent cross-customer data exposure**

Implement safeguards to prevent cross-customer data exposure when combining customer data from multiple sources.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI06 | Memory and Context Poisoning | Primary |

### **A006 \- Prevent PII leakage**

Implement safeguards and technical controls to prevent AI systems from leaking personally identifiable information. PII leakage controls support the memory segmentation and data isolation required to prevent persistent poisoning of shared agent memory.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI06 | Memory and Context Poisoning | Secondary \[R\] |

### **A007 \- Prevent IP violations**

Implement safeguards and technical controls to prevent AI outputs from violating copyrights, trademarks, or other third-party intellectual property rights.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |

## **B. Security**

### **B001 \- Third-party testing of adversarial robustness**

Implement adversarial testing program to validate system resilience against adversarial inputs and prompt injection attempts in line with adversarial threat taxonomy.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI05 | Unexpected Code Execution | Secondary |
| ASI10 | Rogue Agents | Secondary |

### **B002 \- Detect adversarial input**

Implement monitoring capabilities to detect and respond to adversarial inputs and prompt injection attempts.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI05 | Unexpected Code Execution | Secondary \[A\] |

### **B003 \- Manage public release of technical details**

Implement processes to manage the public release of technical details about AI systems to prevent exploitation. Managing disclosure of agent architecture details reduces the attack surface available to adversaries seeking to craft or impersonate rogue agents.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI10 | Rogue Agents | Secondary \[A\] |

### **B004 \- Prevent AI endpoint scraping**

Implement safeguards to prevent adversarial scraping of AI system endpoints. Endpoint scraping can provide adversaries with behavioral knowledge useful for crafting social engineering attacks that exploit user trust.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[A\] |

### **B005 \- Implement real-time input filtering**

Implement real-time input filtering using automated moderation tools.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI05 | Unexpected Code Execution | Secondary |
| ASI06 | Memory and Context Poisoning | Secondary |
| ASI08 | Cascading Failures | Secondary \[A\] |

### **B006 \- Prevent unauthorized AI agent actions**

Implement safeguards to prevent AI agents from performing actions beyond intended scope and authorized privileges.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI08 | Cascading Failures | Primary |
| ASI10 | Rogue Agents | Primary |

B006 is the most broadly mapped requirement in this crosswalk, reflecting the central role of scope enforcement and least-agency controls across the Agentic Top 10\. See the Securing Agentic Applications Guide 1.0 for implementation patterns.

### **B007 \- Enforce user access privileges to AI systems**

Establish and maintain user access controls and admin privileges for AI systems in line with policy.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[A\] |

### **B008 \- Protect model deployment environment**

Implement security measures for AI model deployment environments including encryption, access controls and authorization. Deployment environment protections \- minimal container images, scoped API tokens, TLS, schema validation \- also implement the execution sandbox and egress control requirements called for under tool misuse prevention.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Secondary \[R\] |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI10 | Rogue Agents | Primary |

### **B009 \- Limit output over-exposure**

Implement output limitations and obfuscation techniques to safeguard against information leakage.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI05 | Unexpected Code Execution | Secondary \[A\] |
| ASI06 | Memory and Context Poisoning | Secondary |
| ASI09 | Human-Agent Trust Exploitation | Secondary |
| ASI10 | Rogue Agents | Secondary \[A\] |

## **C. Safety**

### **C002 \- Conduct pre-deployment testing**

Conduct pre-deployment testing to validate AI system safety and security before production release. ASI05 prevention guidelines explicitly call for pre-production checks to prevent direct agent-to-production code execution paths.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI05 | Unexpected Code Execution | Secondary \[R\] |

### **C003 \- Prevent harmful outputs**

Implement safeguards or technical controls to prevent harmful outputs including distressed outputs, angry responses, high-risk advice, offensive content, bias, and deception. C003's explicit coverage of deception prevention directly addresses the core risk of trust exploitation, where ASI09 prevention guidelines call for avoiding persuasive or emotionally manipulative language in safety-critical flows.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI01 | Agent Goal Hijack | Secondary |
| ASI08 | Cascading Failures | Secondary |

### **C004 \- Prevent out-of-scope outputs**

Implement safeguards or technical controls to prevent out-of-scope outputs.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Secondary |
| ASI05 | Unexpected Code Execution | Secondary \[A\] |

### **C005 \- Prevent customer-defined high risk outputs**

Implement safeguards or technical controls to prevent customer-defined high risk outputs. Customer-defined risk categories can serve as supplementary controls when they overlap with agentic threat scenarios such as trust exploitation and unsafe code generation.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI05 | Unexpected Code Execution | Secondary \[A\] |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[A\] |

### **C006 \- Prevent output vulnerabilities**

Implement safeguards to prevent security vulnerabilities in outputs from impacting users.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI05 | Unexpected Code Execution | Primary |
| ASI01 | Agent Goal Hijack | Secondary |

### **C007 \- Flag high risk outputs**

Implement an alerting system that flags high-risk outputs for human review.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI08 | Cascading Failures | Secondary |
| ASI10 | Rogue Agents | Secondary |

### **C008 \- Monitor AI risk categories**

Implement monitoring of AI systems across risk categories.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI10 | Rogue Agents | Secondary |

### **C009 \- Enable real-time feedback and intervention**

Implement mechanisms to enable real-time user feedback collection and intervention mechanisms. C009's pause, stop, and redirect capabilities provide the human-in-the-loop gates called for in ASI01 (human approval for high-impact actions) and ASI08 (human review before agent outputs propagate downstream).

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI01 | Agent Goal Hijack | Secondary \[R\] |
| ASI08 | Cascading Failures | Secondary \[R\] |

### **C010 \- Third-party testing for harmful outputs**

Appoint expert third-parties to evaluate harmful outputs at least every 3 months. As the testing counterpart of C003, C010 validates that harmful output controls \- including deception prevention \- function effectively against trust exploitation scenarios.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[R\] |

### **C011 \- Third-party testing for out-of-scope outputs**

Appoint expert third-parties to evaluate out-of-scope outputs at least every 3 months. As the testing counterpart of C004, C011 validates that scope enforcement controls function effectively against goal hijack scenarios.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Secondary \[R\] |

## **D. Reliability**

### **D001 \- Prevent hallucinated outputs**

Implement safeguards or technical controls to prevent hallucinated outputs.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI08 | Cascading Failures | Primary |
| ASI09 | Human-Agent Trust Exploitation | Primary |

### **D002 \- Third-party testing for hallucinations**

Appoint expert third-parties to evaluate hallucinated outputs at least every 3 months.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI08 | Cascading Failures | Primary |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI10 | Rogue Agents | Secondary \[A\] |

### **D003 \- Restrict unsafe tool calls**

Implement safeguards or technical controls to prevent tool calls in AI systems from executing unauthorized actions, accessing restricted information, or making decisions beyond their intended scope. D003's tool call restrictions are a primary scope enforcement mechanism that directly limits what an escalated-privilege agent can do, addressing ASI03's root cause of "cross-system exploitation due to inadequate scope enforcement."

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI08 | Cascading Failures | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI06 | Memory and Context Poisoning | Secondary |

D003 is one of the most broadly mapped requirements, reflecting the central role of tool-call governance in agentic security. See the CheatSheet on Securely Using Third-Party MCP Servers 1.0 and the Secure MCP Server Development Guide for implementation patterns.

### **D004 \- Third-party testing of tool calls**

Appoint expert third-parties to evaluate tool calls in AI systems at least every 3 months.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI03 | Identity and Privilege Abuse | Secondary |

## **E. Accountability**

### **E001 \- AI failure plan for security breaches**

Document AI failure plan for AI privacy and security breaches assigning accountable owners and establishing notification and remediation.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI08 | Cascading Failures | Primary |
| ASI10 | Rogue Agents | Primary |

### **E002 \- AI failure plan for harmful outputs**

Document AI failure plan for harmful AI outputs that cause significant customer harm.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI08 | Cascading Failures | Primary |

### **E003 \- AI failure plan for hallucinations**

Document AI failure plan for hallucinated AI outputs that cause substantial customer financial loss.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI08 | Cascading Failures | Primary |

### **E005 \- Assess cloud vs on-prem processing**

Establish criteria for selecting cloud provider, and circumstances for on-premises processing.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI04 | Agentic Supply Chain Vulnerabilities | Secondary |

### **E006 \- Conduct vendor due diligence**

Establish AI vendor due diligence processes for foundation and upstream model providers.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |

### **E007 \- Document system change approvals**

Document system change approval processes and maintain approval records. Change approval controls prevent unauthorized modifications to agent systems, supporting the version-controlled prompt and tool governance called for under supply chain integrity.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI04 | Agentic Supply Chain Vulnerabilities | Secondary \[R\] |

### **E009 \- Monitor third-party access**

Implement systems to monitor third party access.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI09 | Human-Agent Trust Exploitation | Secondary \[A\] |

### **E015 \- Log model activity**

Maintain logs of AI system processes, actions, and model outputs to support incident investigation, auditing, and explanation of AI system behavior.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI08 | Cascading Failures | Primary |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI04 | Agentic Supply Chain Vulnerabilities | Secondary \[R\] |
| ASI05 | Unexpected Code Execution | Secondary |

E015 is mapped to all 10 Agentic Top 10 threats (8 Primary, 2 Secondary), reflecting the foundational importance of comprehensive logging for detection, investigation, and accountability across autonomous agent systems.

### **E016 \- Implement AI disclosure mechanisms**

Implement clear disclosure mechanisms to inform users when they are interacting with AI systems rather than humans. Notifying users when autonomous AI agents perform actions (E016.4) enables users to detect and flag unauthorized or rogue agent behavior that would otherwise go unnoticed.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI10 | Rogue Agents | Secondary \[R\] |

## **F. Society**

### **F001 \- Prevent AI cyber misuse**

Implement or document guardrails to prevent AI-enabled misuse for cyber attacks and exploitation. F001's content filtering for malicious code generation and vulnerability exploitation directly prevents agents from generating or executing attack code and limits what a compromised or rogue agent can produce.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI05 | Unexpected Code Execution | Secondary \[R\] |
| ASI10 | Rogue Agents | Secondary \[R\] |

### **F002 \- Prevent catastrophic misuse**

Implement or document guardrails to prevent AI-enabled catastrophic system misuse (chemical / bio / radio / nuclear). F002's monitoring for catastrophic misuse patterns serves as a detection control for the most extreme rogue agent scenarios where agents pursue destructive goals.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI10 | Rogue Agents | Secondary \[R\] |

### **AIUC-1 requirements not mapped to any OWASP Agentic Top 10 item**

The following AIUC-1 requirements do not appear in this crosswalk. This does not mean they are irrelevant to agentic systems \- it means they do not map directly to a specific OWASP Agentic Top 10 threat and either map to the Top 10 for LLM Applications or need additional analysis:

| Code | Requirement | Principle |
| ----- | ----- | ----- |
| A001 | Establish input data policy | A. Data & Privacy |
| A002 | Establish output data policy | A. Data & Privacy |
| C001 | Define AI risk taxonomy | C. Safety |
| C012 | Third-party testing for customer-defined risk | C. Safety |
| E004 | Assign accountability | E. Accountability |
| E008 | Review internal processes | E. Accountability |
| E010 | Establish AI acceptable use policy | E. Accountability |
| E011 | Record processing locations | E. Accountability |
| E012 | Document regulatory compliance | E. Accountability |
| E013 | Implement quality management system | E. Accountability |
| E014 | Share transparency reports | E. Accountability |
| E017 | Document system transparency policy | E. Accountability |

# **Part B \- OWASP Top 10 for Agentic Applications \<-\> AIUC-1 Requirements**

This section starts from each of the 10 OWASP Agentic Top 10 and shows which AIUC-1 requirements address it. This view helps practitioners using the OWASP Top 10 for Agentic Applications refer back to specific AIUC-1 controls.

### **ASI01 \- Agent Goal Hijack**

**OWASP description:** Attackers alter an agent's objectives or decision path through malicious content, exploiting the agent's planning and reasoning capabilities. Hidden prompts can turn copilots into silent exfiltration engines (e.g. EchoLeak). This includes gradual plan injection through subtle sub-goals, direct instruction injection to override original objectives, and reflection loop traps.

**See also:** Agentic AI \- Threats and Mitigations v1.1; Securing Agentic Applications Guide 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B001 | Third-party testing of adversarial robustness | Primary |
| B002 | Detect adversarial input | Primary |
| B005 | Implement real-time input filtering | Primary |
| B006 | Prevent unauthorized AI agent actions | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| E015 | Log model activity | Primary |
| C003 | Prevent harmful outputs | Secondary |
| C004 | Prevent out-of-scope outputs | Secondary |
| C006 | Prevent output vulnerabilities | Secondary |
| C009 | Enable real-time feedback and intervention | Secondary \[R\] |
| C011 | Third-party testing for out-of-scope outputs | Secondary \[R\] |

### **ASI02 \- Tool Misuse and Exploitation**

**OWASP description:** Agents use legitimate tools in unsafe ways due to ambiguous prompts, misalignment, or manipulated input. This can cause agents to call tools with destructive parameters or chain tools together in unexpected sequences leading to data loss or exfiltration (e.g. Amazon Q incident). Includes parameter pollution, tool chain manipulation, and automated abuse of granted permissions.

**See also:** CheatSheet \- Securely Using Third-Party MCP Servers 1.0; Secure MCP Server Development Guide; Securing Agentic Applications Guide 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| A003 | Limit AI agent data collection | Primary |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B007 | Enforce user access privileges to AI systems | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| D004 | Third-party testing of tool calls | Primary |
| E009 | Monitor third-party access | Primary |
| E015 | Log model activity | Primary |
| B008 | Protect model deployment environment | Secondary \[R\] |

### **ASI03 \- Identity and Privilege Abuse**

**OWASP description:** Agents inherit user or system identities with high-privilege credentials, creating opportunities for privilege escalation and unauthorized access across systems. Leaked credentials allow agents to operate far beyond their intended scope. Includes dynamic permission escalation, cross-system exploitation due to inadequate scope enforcement, and shadow agent deployment that inherits legitimate credentials.

**See also:** Securing Agentic Applications Guide 1.0; Agent Name Service (ANS) v1.0; State of Agentic AI Security and Governance 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B007 | Enforce user access privileges to AI systems | Primary |
| B008 | Protect model deployment environment | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| E009 | Monitor third-party access | Primary |
| E015 | Log model activity | Primary |
| D004 | Third-party testing of tool calls | Secondary |

### **ASI04 \- Agentic Supply Chain Vulnerabilities**

**OWASP description:** Compromised tools, plugins, MCP services, model APIs, datasets, open-source packages, and external agents introduce vulnerabilities that agents may unknowingly leverage (e.g. GitHub MCP exploit). A compromise anywhere upstream cascades into the primary agent. Supply chain vulnerabilities are amplified because autonomous agents reuse compromised data and tools repeatedly and at scale.

**See also:** CheatSheet \- Securely Using Third-Party MCP Servers 1.0; Secure MCP Server Development Guide; Agent Name Service (ANS) v1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| A004 | Protect IP & trade secrets | Primary |
| A007 | Prevent IP violations | Primary |
| B008 | Protect model deployment environment | Primary |
| E006 | Conduct vendor due diligence | Primary |
| E009 | Monitor third-party access | Primary |
| E005 | Assess cloud vs on-prem processing | Secondary |
| E007 | Document system change approvals | Secondary \[R\] |
| E015 | Log model activity | Secondary \[R\] |

### **ASI05 \- Unexpected Code Execution**

**OWASP description:** Agents generate or run code and commands unsafely, creating opportunities for remote code execution, sandbox escapes, and data exfiltration (e.g. AutoGPT RCE). Natural-language execution paths unlock dangerous avenues for RCE delivered through prompts instead of traditional exploits, turning agents into remote execution gateways.

**See also:** Securing Agentic Applications Guide 1.0; Agentic AI \- Threats and Mitigations v1.1

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B008 | Protect model deployment environment | Primary |
| C006 | Prevent output vulnerabilities | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| D004 | Third-party testing of tool calls | Primary |
| B001 | Third-party testing of adversarial robustness | Secondary |
| B002 | Detect adversarial input | Secondary \[A\] |
| B005 | Implement real-time input filtering | Secondary |
| B009 | Limit output over-exposure | Secondary \[A\] |
| C002 | Conduct pre-deployment testing | Secondary \[R\] |
| C004 | Prevent out-of-scope outputs | Secondary \[A\] |
| C005 | Prevent customer-defined high risk outputs | Secondary \[A\] |
| E015 | Log model activity | Secondary |
| F001 | Prevent AI cyber misuse | Secondary \[R\] |

### **ASI06 \- Memory and Context Poisoning**

**OWASP description:** Attackers poison agent memory systems, embeddings, and RAG databases to corrupt stored information and manipulate decision-making across sessions (e.g. Gemini Memory Attack). Unlike prompt injection, memory poisoning is persistent \- the agent continues to behave incorrectly long after the initial attack. Includes gradual memory poisoning through repeated interactions and corrupting shared memory in multi-agent systems.

**See also:** Agentic AI \- Threats and Mitigations v1.1; Multi-Agentic System Threat Modeling Guide v1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| A003 | Limit AI agent data collection | Primary |
| A005 | Prevent cross-customer data exposure | Primary |
| B001 | Third-party testing of adversarial robustness | Primary |
| B002 | Detect adversarial input | Primary |
| B006 | Prevent unauthorized AI agent actions | Primary |
| E015 | Log model activity | Primary |
| A006 | Prevent PII leakage | Secondary \[R\] |
| B005 | Implement real-time input filtering | Secondary |
| B009 | Limit output over-exposure | Secondary |
| D003 | Restrict unsafe tool calls | Secondary |

### **ASI07 \- Insecure Inter-Agent Communication**

**OWASP description:** Multi-agent systems face spoofed identities, replayed messages, and tampering in communication channels between agents. Spoofed inter-agent messages can misdirect entire clusters. If communication channels are not authenticated, encrypted, or validated, attackers can impersonate trusted agents and influence entire multi-agent systems.

**See also:** Multi-Agentic System Threat Modeling Guide v1.0; Agent Name Service (ANS) v1.0; Securing Agentic Applications Guide 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B007 | Enforce user access privileges to AI systems | Primary |
| B008 | Protect model deployment environment | Primary |
| E009 | Monitor third-party access | Primary |
| E015 | Log model activity | Primary |

**Observed AIUC-1 gap:** The OWASP entry and the Multi-Agentic System Threat Modeling Guide emphasize mutual authentication, message integrity, replay protection, signed agent cards, attested registries, and protocol/version pinning for inter-agent communication. The Agent Name Service (ANS) proposes a PKI-based framework for addressing agent discovery and identity. AIUC-1 does not currently expose a dedicated requirement for end-to-end authentication and attestation of inter-agent communications. The team should evaluate whether a new requirement is warranted (e.g. "Secure inter-agent communication channels").

### **ASI08 \- Cascading Failures**

**OWASP description:** Small errors in one agent propagate across planning, execution, and memory, amplifying through interconnected systems. False signals cascade through automated pipelines with escalating impact. Includes injecting false data that accumulates in long-term memory, introducing hallucinated API endpoints that cause data leaks, and implanting false information that worsens through self-reinforcement.

**See also:** Agentic AI \- Threats and Mitigations v1.1; Multi-Agentic System Threat Modeling Guide v1.0; Securing Agentic Applications Guide 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| D001 | Prevent hallucinated outputs | Primary |
| D002 | Third-party testing for hallucinations | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| E001 | AI failure plan for security breaches | Primary |
| E002 | AI failure plan for harmful outputs | Primary |
| E003 | AI failure plan for hallucinations | Primary |
| E015 | Log model activity | Primary |
| B005 | Implement real-time input filtering | Secondary \[A\] |
| C003 | Prevent harmful outputs | Secondary |
| C007 | Flag high risk outputs | Secondary |
| C009 | Enable real-time feedback and intervention | Secondary \[R\] |

**Observed AIUC-1 gap:** ASI08 prevention guidelines call for circuit breakers between planner and executor, blast-radius guardrails (quotas, progress caps), digital twin replay testing, and independent policy enforcement separating planning from execution. AIUC-1 covers failure response plans (E001-E003) and output validation (C007), but does not require architectural containment mechanisms that prevent error propagation between interconnected agents and systems. The team should evaluate whether a new requirement is warranted (e.g. "Implement cascading failure containment controls").

### **ASI09 \- Human-Agent Trust Exploitation**

**OWASP description:** Users over-trust agent recommendations or explanations, enabling social engineering and covert harmful actions. Confident, polished explanations mislead human operators into approving harmful actions. Includes AI-powered invoice fraud replacing legitimate vendor details, AI-driven phishing with deceptive messages, and misinformation campaigns through trusted agent interfaces.

**See also:** State of Agentic AI Security and Governance 1.0; Agentic AI \- Threats and Mitigations v1.1

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| C003 | Prevent harmful outputs | Primary |
| C007 | Flag high risk outputs | Primary |
| C009 | Enable real-time feedback and intervention | Primary |
| D001 | Prevent hallucinated outputs | Primary |
| D002 | Third-party testing for hallucinations | Primary |
| E015 | Log model activity | Primary |
| E016 | Implement AI disclosure mechanisms | Primary |
| A003 | Limit AI agent data collection | Secondary \[A\] |
| B004 | Prevent AI endpoint scraping | Secondary \[A\] |
| B007 | Enforce user access privileges to AI systems | Secondary \[A\] |
| B009 | Limit output over-exposure | Secondary |
| C005 | Prevent customer-defined high risk outputs | Secondary \[A\] |
| C010 | Third-party testing for harmful outputs | Secondary \[R\] |
| E009 | Monitor third-party access | Secondary \[A\] |

### **ASI10 \- Rogue Agents**

**OWASP description:** Compromised or misaligned agents act harmfully while appearing legitimate. They may self-repeat actions, persist across sessions, or impersonate other agents (e.g. Replit meltdown). Some agents exhibit misalignment, concealment, and self-directed action. Includes malicious workflow injection impersonating approval agents, orchestration hijacking for fraudulent transactions, and coordinated agent flooding.

**See also:** Multi-Agentic System Threat Modeling Guide v1.0; Agent Name Service (ANS) v1.0; Agentic AI \- Threats and Mitigations v1.1

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B007 | Enforce user access privileges to AI systems | Primary |
| B008 | Protect model deployment environment | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| D004 | Third-party testing of tool calls | Primary |
| E001 | AI failure plan for security breaches | Primary |
| E015 | Log model activity | Primary |
| B001 | Third-party testing of adversarial robustness | Secondary |
| B003 | Manage public release of technical details | Secondary \[A\] |
| B009 | Limit output over-exposure | Secondary \[A\] |
| C007 | Flag high risk outputs | Secondary |
| C008 | Monitor AI risk categories | Secondary |
| D002 | Third-party testing for hallucinations | Secondary \[A\] |
| E016 | Implement AI disclosure mechanisms | Secondary \[R\] |
| F001 | Prevent AI cyber misuse | Secondary \[R\] |
| F002 | Prevent catastrophic misuse | Secondary \[R\] |

**Observed AIUC-1 gap:** The OWASP entry and the Multi-Agentic System Threat Modeling Guide emphasize per-agent cryptographic identity attestation, signed behavioral manifests, kill switches, credential revocation, trust zones, and reintegration checks. The Agent Name Service (ANS) proposes PKI-based agent identity verification relevant to detecting rogue agents. AIUC-1 does not currently expose dedicated requirements for agent-level attestation, behavioral manifests, or runtime kill-switch mechanisms. The team should evaluate whether new requirements are warranted (e.g. "Implement agent identity attestation" or "Implement agent kill-switch / containment controls").

## **Observed AIUC-1 gaps**

Based on this crosswalk exercise, four areas where AIUC-1 may benefit from new or expanded requirements:

**1\. Inter-agent communication security (surfaces at ASI07, ASI10)**

The OWASP Multi-Agentic System Threat Modeling Guide and Agent Name Service (ANS) describe needs for mutual authentication, message integrity, replay protection, signed agent cards, and attested registries. AIUC-1 does not currently have a dedicated requirement for securing agent-to-agent communication channels.

**2\. Agent identity attestation and containment (surfaces at ASI10, ASI03)**

The OWASP suite describes per-agent cryptographic identity, signed behavioral manifests, kill switches, credential revocation, trust zones, and reintegration checks. AIUC-1 does not currently have a dedicated requirement for agent-level identity attestation or runtime containment/kill-switch mechanisms.

**3\. Agentic supply chain attestation (surfaces at ASI04, ASI02)**

ASI04 prevention guidelines call for signed manifests (SBOMs/AIBOMs), prompt provenance tracking, content-hash pinning for tools and configurations, and staged rollout with differential testing. AIUC-1 covers vendor due diligence (E006) and change approvals (E007) but does not require attestation artifacts specific to agentic components: tool manifests, prompt version control, or agent dependency bills of materials.

**4\. Cascading failure containment mechanisms (surfaces at ASI08)**

ASI08 prevention guidelines call for circuit breakers between planner and executor, blast-radius guardrails (quotas, progress caps), digital twin replay testing, and independent policy enforcement separating planning from execution. AIUC-1 covers failure response plans (E001-E003) and output validation (C007), but does not require architectural containment mechanisms \- such as circuit breakers, blast-radius caps, or planner-executor isolation \- that prevent error propagation between interconnected agents.

# **Notes for contributors & reviewers**

1. **Consistency** \- Parts A and B are generated from the same underlying mapping data (105 total mappings: 62 Primary, 43 Secondary). Any changes must be applied to both parts.
2. **Primary vs Secondary labels** \- Validate the relevance classifications. Move requirements between tiers as needed based on team expertise.
3. **Provenance markers** \- 13 mappings marked \[A\] originated from automated analysis; 13 mappings marked \[R\] were added during review against OWASP prevention guidelines. Both sets merit scrutiny: upgrade to Primary, retain as Secondary, or remove as appropriate.
4. **Coverage gaps** \- Four gaps are explicitly called out (ASI07, ASI10, ASI04, ASI08). Are there others? Consider whether new AIUC-1 requirements are needed for inter-agent authentication, agent identity attestation, supply chain attestation, circuit breakers, or blast-radius containment.
5. **Remaining unmapped requirements** \- 12 requirements have no mapping. The E-category governance controls (E004, E008, E010-E014, E017) are generally policy and process requirements that do not map directly to specific agentic threats. A001, A002 (data policy), C001 (risk taxonomy), and C012 (third-party testing for customer-defined risk) may warrant future review.
6. **OWASP resource references** \- Verify that the "See also" references under each threat accurately reflect the most relevant companion documents.
