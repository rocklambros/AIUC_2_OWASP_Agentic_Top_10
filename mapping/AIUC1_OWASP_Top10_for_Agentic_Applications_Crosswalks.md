# AIUC-1 \- OWASP Top10 for Agentic Applications \- Crosswalks.

**DRAFT**

**Document log**

| Date | Author | Contribution |
| :---- | :---- | :---- |
| **March 15, 2026** | **John Sotiropoulos** | **Initial Draft** |
|  |  |  |
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

This section starts from each AIUC-1 requirement and shows which OWASP Agentic Top 10 threats it addresses. The crosswalk allows AIUC1 practitioners to find and use the appropriate OWASP Agentic Top 10 items and understand the relevant threat and mitigations. Only requirements with at least one mapping are listed. Requirements with no mapping to the OWASP Top 10 for Agentic Applications  are listed at the end of this section.

## **A. Data & Privacy**

### **A003 \- Limit AI agent data collection**

Implement safeguards to limit AI agent data access to task-relevant information based on user roles and context.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI06 | Memory and Context Poisoning | Primary |

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

### **B005 \- Implement real-time input filtering**

Implement real-time input filtering using automated moderation tools.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI05 | Unexpected Code Execution | Secondary |
| ASI06 | Memory and Context Poisoning | Secondary |

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

B006 is the most broadly mapped requirement in this crosswalk, reflecting the central role of scope enforcement and least-agency controls across Agentic Top 10\. See the Securing Agentic Applications Guide 1.0 for implementation patterns.

### **B007 \- Enforce user access privileges to AI systems**

Establish and maintain user access controls and admin privileges for AI systems in line with policy.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI10 | Rogue Agents | Primary |

### **B008 \- Protect model deployment environment**

Implement security measures for AI model deployment environments including encryption, access controls and authorization.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI10 | Rogue Agents | Primary |

### **B009 \- Limit output over-exposure**

Implement output limitations and obfuscation techniques to safeguard against information leakage.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI06 | Memory and Context Poisoning | Secondary |
| ASI09 | Human-Agent Trust Exploitation | Secondary |

## **C. Safety**

### **C003 \- Prevent harmful outputs**

Implement safeguards or technical controls to prevent harmful outputs including distressed outputs, angry responses, high-risk advice, offensive content, bias, and deception.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Secondary |
| ASI08 | Cascading Failures | Secondary |
| ASI09 | Human-Agent Trust Exploitation | Secondary |

### **C004 \- Prevent out-of-scope outputs**

Implement safeguards or technical controls to prevent out-of-scope outputs.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Secondary |

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

Implement mechanisms to enable real-time user feedback collection and intervention mechanisms.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |

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

### **D003 \- Restrict unsafe tool calls**

Implement safeguards or technical controls to prevent tool calls in AI systems from executing unauthorized actions, accessing restricted information, or making decisions beyond their intended scope.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI05 | Unexpected Code Execution | Primary |
| ASI08 | Cascading Failures | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI03 | Identity and Privilege Abuse | Secondary |
| ASI06 | Memory and Context Poisoning | Secondary |

D003 is the second most broadly mapped requirement, reflecting the central role of tool-call governance in agentic security. See the CheatSheet on Securely Using Third-Party MCP Servers 1.0 and the Secure MCP Server Development Guide for implementation patterns.

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

### **E009 \- Monitor third-party access**

Implement systems to monitor third party access.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI02 | Tool Misuse and Exploitation | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI04 | Agentic Supply Chain Vulnerabilities | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |

### **E015 \- Log model activity**

Maintain logs of AI system processes, actions, and model outputs to support incident investigation, auditing, and explanation of AI system behavior.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI01 | Agent Goal Hijack | Primary |
| ASI03 | Identity and Privilege Abuse | Primary |
| ASI06 | Memory and Context Poisoning | Primary |
| ASI07 | Insecure Inter-Agent Communication | Primary |
| ASI08 | Cascading Failures | Primary |
| ASI09 | Human-Agent Trust Exploitation | Primary |
| ASI10 | Rogue Agents | Primary |
| ASI02 | Tool Misuse and Exploitation | Secondary |
| ASI05 | Unexpected Code Execution | Secondary |

E015 is mapped to all 10 Agentic Top 10 (7 Primary, 2 Secondary), reflecting the foundational importance of comprehensive logging for detection, investigation, and accountability across autonomous agent systems.

### **E016 \- Implement AI disclosure mechanisms**

Implement clear disclosure mechanisms to inform users when they are interacting with AI systems rather than humans.

| OWASP Threat | Threat Name | Relevance |
| ----- | ----- | ----- |
| ASI09 | Human-Agent Trust Exploitation | Primary |

## **F. Society**

No F-category requirements are currently mapped to the OWASP Top 10 for Agentic Applications. The team should review whether F001 (Prevent AI cyber misuse) and F002 (Prevent catastrophic misuse) are relevant to specific threats, particularly ASI05 (Unexpected Code Execution) and ASI10 (Rogue Agents).

### **AIUC-1 requirements not mapped to any OWASP Agentic Top Item**

The following AIUC-1 requirements do not appear in this crosswalk. This does not mean they are irrelevant to agentic systems \- it means they do not map directly to a specific OWASP Agentic Top 10 threat and either map to the Top 10 for LLM Applications or need extra work to map tjemt:

| Code | Requirement | Principle |
| ----- | ----- | ----- |
| A001 | Establish input data policy | A. Data & Privacy |
| A002 | Establish output data policy | A. Data & Privacy |
| A006 | Prevent PII leakage | A. Data & Privacy |
| B003 | Manage public release of technical details | B. Security |
| B004 | Prevent AI endpoint scraping | B. Security |
| C001 | Define AI risk taxonomy | C. Safety |
| C002 | Conduct pre-deployment testing | C. Safety |
| C005 | Prevent customer-defined high risk outputs | C. Safety |
| C010 | Third-party testing for harmful outputs | C. Safety |
| C011 | Third-party testing for out-of-scope outputs | C. Safety |
| C012 | Third-party testing for customer-defined risk | C. Safety |
| E004 | Assign accountability | E. Accountability |
| E008 | Review internal processes | E. Accountability |
| E010 | Establish AI acceptable use policy | E. Accountability |
| E011 | Record processing locations | E. Accountability |
| E012 | Document regulatory compliance | E. Accountability |
| E013 | Implement quality management system | E. Accountability |
| E017 | Document system transparency policy | E. Accountability |
| F001 | Prevent AI cyber misuse | F. Society |
| F002 | Prevent catastrophic misuse | F. Society |

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
| E015 | Log model activity | Secondary |

### **ASI03 \- Identity and Privilege Abuse**

**OWASP description:** Agents inherit user or system identities with high-privilege credentials, creating opportunities for privilege escalation and unauthorized access across systems. Leaked credentials allow agents to operate far beyond their intended scope. Includes dynamic permission escalation, cross-system exploitation due to inadequate scope enforcement, and shadow agent deployment that inherits legitimate credentials.

**See also:** Securing Agentic Applications Guide 1.0; Agent Name Service (ANS) v1.0; State of Agentic AI Security and Governance 1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B006 | Prevent unauthorized AI agent actions | Primary |
| B007 | Enforce user access privileges to AI systems | Primary |
| B008 | Protect model deployment environment | Primary |
| E009 | Monitor third-party access | Primary |
| E015 | Log model activity | Primary |
| D003 | Restrict unsafe tool calls | Secondary |
| D004 | Third-party testing of tool calls | Secondary |

### **ASI04 \- Agentic Supply Chain Vulnerabilities**

**OWASP description:** Compromised tools, plugins, MCP services, model APIs, datasets, open-source packages, and external agents introduce vulnerabilities that agents may unknowingly leverage (e.g. GitHub MCP exploit). A compromise anywhere upstream cascades into the primary agent. Supply chain vulnerabilities are amplified because autonomous agents reuse compromised data and tools repeatedly and at scale.

**See also:** CheatSheet \- Securely Using Third-Party MCP Servers 1.0; Secure MCP Server Development Guide; Agent Name Service (ANS) v1.0

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| E006 | Conduct vendor due diligence | Primary |
| E009 | Monitor third-party access | Primary |
| B008 | Protect model deployment environment | Primary |
| A004 | Protect IP & trade secrets | Primary |
| A007 | Prevent IP violations | Primary |
| E005 | Assess cloud vs on-prem processing | Secondary |

### **ASI05 \- Unexpected Code Execution**

**OWASP description:** Agents generate or run code and commands unsafely, creating opportunities for remote code execution, sandbox escapes, and data exfiltration (e.g. AutoGPT RCE). Natural-language execution paths unlock dangerous avenues for RCE delivered through prompts instead of traditional exploits, turning agents into remote execution gateways.

**See also:** Securing Agentic Applications Guide 1.0; Agentic AI \- Threats and Mitigations v1.1

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| B008 | Protect model deployment environment | Primary |
| B006 | Prevent unauthorized AI agent actions | Primary |
| D003 | Restrict unsafe tool calls | Primary |
| D004 | Third-party testing of tool calls | Primary |
| C006 | Prevent output vulnerabilities | Primary |
| B001 | Third-party testing of adversarial robustness | Secondary |
| B005 | Implement real-time input filtering | Secondary |
| E015 | Log model activity | Secondary |

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
| C003 | Prevent harmful outputs | Secondary |
| C007 | Flag high risk outputs | Secondary |

### **ASI09 \- Human-Agent Trust Exploitation**

**OWASP description:** Users over-trust agent recommendations or explanations, enabling social engineering and covert harmful actions. Confident, polished explanations mislead human operators into approving harmful actions. Includes AI-powered invoice fraud replacing legitimate vendor details, AI-driven phishing with deceptive messages, and misinformation campaigns through trusted agent interfaces.

**See also:** State of Agentic AI Security and Governance 1.0; Agentic AI \- Threats and Mitigations v1.1

**Relevant AIUC-1 requirements:**

| Code | Requirement | Relevance |
| ----- | ----- | ----- |
| E016 | Implement AI disclosure mechanisms | Primary |
| C009 | Enable real-time feedback and intervention | Primary |
| C007 | Flag high risk outputs | Primary |
| D001 | Prevent hallucinated outputs | Primary |
| D002 | Third-party testing for hallucinations | Primary |
| E015 | Log model activity | Primary |
| C003 | Prevent harmful outputs | Secondary |
| B009 | Limit output over-exposure | Secondary |

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
| C007 | Flag high risk outputs | Secondary |
| C008 | Monitor AI risk categories | Secondary |

**Observed AIUC-1 gap:** The OWASP entry and the Multi-Agentic System Threat Modeling Guide emphasize per-agent cryptographic identity attestation, signed behavioral manifests, kill switches, credential revocation, trust zones, and reintegration checks. The Agent Name Service (ANS) proposes PKI-based agent identity verification relevant to detecting rogue agents. AIUC-1 does not currently expose dedicated requirements for agent-level attestation, behavioral manifests, or runtime kill-switch mechanisms. The team should evaluate whether new requirements are warranted (e.g. "Implement agent identity attestation" or "Implement agent kill-switch / containment controls").

## **Observed AIUC-1 gaps**

Based on this crosswalk exercise, two areas where AIUC-1 may benefit from new or expanded requirements:

**1\. Inter-agent communication security (surfaces at ASI07, ASI10)**

The OWASP Multi-Agentic System Threat Modeling Guide and Agent Name Service (ANS) describe needs for mutual authentication, message integrity, replay protection, signed agent cards, and attested registries. AIUC-1 does not currently have a dedicated requirement for securing agent-to-agent communication channels.

**2\. Agent identity attestation and containment (surfaces at ASI10, ASI03)**

The OWASP suite describes per-agent cryptographic identity, signed behavioral manifests, kill switches, credential revocation, trust zones, and reintegration checks. AIUC-1 does not currently have a dedicated requirement for agent-level identity attestation or runtime containment/kill-switch mechanisms.

# **Notes for contributors & reviewers**

1. **Consistency** \- Parts A and B are generated from the same underlying mapping data (79 total mappings: 59 Primary, 20 Secondary). Any changes must be applied to both parts.  
2. **Primary vs Secondary labels** \- Validate the relevance classifications. Move requirements between tiers as needed based on team expertise.  
3. **Coverage gaps** \- Two gaps are explicitly called out (ASI07 and ASI10). Are there others? Consider whether new AIUC-1 requirements are needed for inter-agent authentication, agent identity attestation, kill switches, or circuit breakers.  
4. **Unmapped requirements** \- Review the "not mapped" table in Part A. Some requirements (e.g. A006 Prevent PII leakage, C002 Conduct pre-deployment testing) may deserve inclusion under specific threats.  
5. **OWASP resource references** \- Verify that the "See also" references under each threat accurately reflect the most relevant companion documents.

