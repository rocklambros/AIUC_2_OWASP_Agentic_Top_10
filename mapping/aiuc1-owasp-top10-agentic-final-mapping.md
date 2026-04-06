# **APPENDIX A \- Mapping rationale taxonomy and master table**

This appendix provides the rationale for every mapping in the crosswalk. Each mapping carries a rationale code indicating the control function it provides against the mapped threat. Part A and Part B tables are generated from this master data.

## Rationale taxonomy

| Code | Label | Definition |
| :---- | :---- | :---- |
| PREV | Prevent | Directly blocks or stops the core attack mechanism before it succeeds (e.g., input filtering blocks injection payloads, output filtering catches malicious content, disclosure controls limit attacker reconnaissance). |
| SCOPE | Constrain scope | Limits what a compromised or misbehaving agent can reach, reducing blast radius after an attack succeeds (e.g., least privilege, data minimization, tool-call restrictions, access controls). |
| GATE | Human gate | Enforces a human approval, review, or intervention point that the threat's prevention guidelines specifically require (e.g., pause/stop controls, confirmation for high-impact actions, flagging high-risk outputs for review). |
| DETECT | Detect and trace | Provides runtime detection, behavioral monitoring, or forensic traceability for the threat (e.g., logging, anomaly detection, detection of deviation from behavioral baselines, third-party access monitoring). |
| VALID | Validate and test | Tests, audits, or validates that other controls function effectively against the threat (e.g., third-party adversarial testing, red-team exercises, tool-call testing, vendor due diligence). |
| GOVERN | Policy and governance | Establishes the organizational policy, accountability, process framework, or response plan that supports technical controls against the threat (e.g., acceptable use policies, assigned accountability, change approvals, failure response plans). |
| ISOLATE | Isolate and contain | Enforces architectural separation that prevents the threat from propagating across agents, sessions, tenants, or systems (e.g., memory segmentation, tenant isolation, deployment environment hardening, container sandboxing). |
| DISCLOSE | Disclose and calibrate | Provides transparency, provenance, or disclosure mechanisms that enable humans to calibrate trust and detect deception (e.g., AI disclosure mechanisms, model cards, content provenance, interpretability reports). |

Primary vs Secondary is determined by the threat context, not the rationale code. PREV and SCOPE mappings tend to be Primary. DETECT and GOVERN tend to be Secondary. The threat determines the final call: DETECT is Primary for ASI06 (memory poisoning is invisible without logging) but Secondary for ASI01 (where preventive controls are the frontline).

## Master mapping table

### ASI01 \- Agent Goal Hijack

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B001 | Third-party testing of adversarial robustness | Primary | VALID |
| B002 | Detect adversarial input | Primary | PREV Madjid\>”DETECT”? |
| B005 | Implement real-time input filtering | Primary | PREV |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE Madjid\>\>+PREV |
| C009 | Enable real-time feedback and intervention | Primary | GATE |
| D003 | Restrict unsafe tool calls | Primary | SCOPE Madjid\>\>+PREV |
| A004 | Protect IP & trade secrets | Secondary | SCOPE |
| C002 | Conduct pre-deployment testing | Secondary | VALID |
| C003 | Prevent harmful outputs | Secondary | PREV |
| C004 | Prevent out-of-scope outputs | Secondary | PREV |
| C006 | Prevent output vulnerabilities | Secondary | PREV |
| C011 | Third-party testing for out-of-scope outputs | Secondary | VALID |
| E008 | Review internal processes | Secondary | GOVERN |
| E010 | Establish AI acceptable use policy | Secondary | GOVERN |
| E015 | Log model activity | Secondary | DETECT |

### ASI02 \- Tool Misuse and Exploitation

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| A003 | Limit AI agent data collection | Primary | SCOPE |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE And PREV |
| B007 | Enforce user access privileges to AI systems | Primary | SCOPE |
| D003 | Restrict unsafe tool calls | Primary | SCOPE And PREV |
| D004 | Third-party testing of tool calls | Primary | VALID |
| E009 | Monitor third-party access | Primary | DETECT |
| A004 | Protect IP & trade secrets | Secondary | SCOPE |
| A007 | Prevent IP violations | Secondary | SCOPE |
| B008 | Protect model deployment environment | Secondary | ISOLATE |
| C009 | Enable real-time feedback and intervention | Secondary | GATE |
| E015 | Log model activity | Secondary | DETECT |

### ASI03 \- Identity and Privilege Abuse

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE |
| B007 | Enforce user access privileges to AI systems | Primary | SCOPE |
| B008 | Protect model deployment environment | Primary | ISOLATE |
| D003 | Restrict unsafe tool calls | Primary | SCOPE |
| E009 | Monitor third-party access | Primary | DETECT |
| A004 | Protect IP & trade secrets | Secondary | SCOPE |
| A007 | Prevent IP violations | Secondary | SCOPE |
| B003 | Manage public release of technical details | Secondary | PREV |
| D004 | Third-party testing of tool calls | Secondary | VALID |
| E010 | Establish AI acceptable use policy | Secondary | GOVERN |
| E015 | Log model activity | Secondary | DETECT |

### ASI04 \- Agentic Supply Chain Vulnerabilities

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B008 | Protect model deployment environment | Primary | ISOLATE |
| E006 | Conduct vendor due diligence | Primary | VALID |
| E009 | Monitor third-party access | Primary | DETECT |
| A004 | Protect IP & trade secrets | Secondary | SCOPE |
| A007 | Prevent IP violations | Secondary | SCOPE |
| E005 | Assess cloud vs on-prem processing | Secondary | GOVERN |
| E007 | Document system change approvals | Secondary | GOVERN |
| E015 | Log model activity | Secondary | DETECT |

### ASI05 \- Unexpected Code Execution

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE |
| B008 | Protect model deployment environment | Primary | ISOLATE |
| C006 | Prevent output vulnerabilities | Primary | PREV |
| D003 | Restrict unsafe tool calls | Primary | SCOPE |
| D004 | Third-party testing of tool calls | Primary | VALID |
| B001 | Third-party testing of adversarial robustness | Secondary | VALID |
| B002 | Detect adversarial input | Secondary \[A\] | PREV |
| B005 | Implement real-time input filtering | Secondary | PREV |
| B009 | Limit output over-exposure | Secondary \[A\] | SCOPE |
| C002 | Conduct pre-deployment testing | Secondary | VALID |
| C004 | Prevent out-of-scope outputs | Secondary \[A\] | PREV |
| C005 | Prevent customer-defined high risk outputs | Secondary \[A\] | PREV |
| E015 | Log model activity | Secondary | DETECT |
| F001 | Prevent AI cyber misuse | Secondary | PREV |

### ASI06 \- Memory and Context Poisoning

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| A003 | Limit AI agent data collection | Primary | SCOPE |
| A005 | Prevent cross-customer data exposure | Primary | ISOLATE |
| B001 | Third-party testing of adversarial robustness | Primary | VALID |
| B002 | Detect adversarial input | Primary | PREV |
| B005 | Implement real-time input filtering | Primary | PREV |
| E015 | Log model activity | Primary | DETECT |
| A006 | Prevent PII leakage | Secondary | ISOLATE |
| B006 | Prevent unauthorized AI agent actions | Secondary | SCOPE |
| B009 | Limit output over-exposure | Secondary | SCOPE |
| D003 | Restrict unsafe tool calls | Secondary | SCOPE |

### ASI07 \- Insecure Inter-Agent Communication

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE |
| B008 | Protect model deployment environment | Primary | ISOLATE |
| E009 | Monitor third-party access | Primary | DETECT |
| E015 | Log model activity | Primary | DETECT |
| ASI07 |  Insecure Inter-Agent Communication | Secondary | SCOPE |

### ASI08 \- Cascading Failures

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| D001 | Prevent hallucinated outputs | Primary | PREV |
| D002 | Third-party testing for hallucinations | Primary | VALID |
| D003 | Restrict unsafe tool calls | Primary | SCOPE |
| E001 | AI failure plan for security breaches | Primary | GOVERN |
| E002 | AI failure plan for harmful outputs | Primary | GOVERN |
| E003 | AI failure plan for hallucinations | Primary | GOVERN |
| E015 | Log model activity | Primary | DETECT |
| B005 | Implement real-time input filtering | Secondary \[A\] | PREV |
| B006 | Prevent unauthorized AI agent actions | Secondary | SCOPE |
| C003 | Prevent harmful outputs | Secondary | PREV |
| C007 | Flag high risk outputs | Secondary | GATE |
| C009 | Enable real-time feedback and intervention | Secondary | GATE |

### ASI09 \- Human-Agent Trust Exploitation

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| C003 | Prevent harmful outputs | Primary | PREV |
| C007 | Flag high risk outputs | Primary | GATE |
| C009 | Enable real-time feedback and intervention | Primary | GATE |
| C010 | Third-party testing for harmful outputs | Primary | VALID |
| D001 | Prevent hallucinated outputs | Primary | PREV |
| D002 | Third-party testing for hallucinations | Primary | VALID |
| E016 | Implement AI disclosure mechanisms | Primary | DISCLOSE |
| A003 | Limit AI agent data collection | Secondary \[A\] | SCOPE |
| B004 | Prevent AI endpoint scraping | Secondary \[A\] | PREV |
| B007 | Enforce user access privileges to AI systems | Secondary \[A\] | SCOPE |
| B009 | Limit output over-exposure | Secondary | SCOPE |
| C005 | Prevent customer-defined high risk outputs | Secondary \[A\] | PREV |
| C006 | Prevent output vulnerabilities | Secondary | PREV |
| E004 | Assign accountability | Secondary | GOVERN |
| E009 | Monitor third-party access | Secondary \[A\] | DETECT |
| E015 | Log model activity | Secondary | DETECT |
| E017 | Document system transparency policy | Secondary | DISCLOSE |

### ASI10 \- Rogue Agents

| AIUC-1 Code | Requirement | Relevance | Rationale |
| :---- | :---- | :---- | :---- |
| B006 | Prevent unauthorized AI agent actions | Primary | SCOPE |
| B008 | Protect model deployment environment | Primary | ISOLATE |
| D003 | Restrict unsafe tool calls | Primary | SCOPE |
| D004 | Third-party testing of tool calls | Primary | VALID |
| E001 | AI failure plan for security breaches | Primary | GOVERN |
| E015 | Log model activity | Primary | DETECT |
| B001 | Third-party testing of adversarial robustness | Secondary | VALID |
| B003 | Manage public release of technical details | Secondary \[A\] | PREV |
| B007 | Enforce user access privileges to AI systems | Secondary | SCOPE |
| B009 | Limit output over-exposure | Secondary \[A\] | SCOPE |
| C007 | Flag high risk outputs | Secondary | GATE |
| C008 | Monitor AI risk categories | Secondary | DETECT |
| C009 | Enable real-time feedback and intervention | Secondary | GATE |
| D002 | Third-party testing for hallucinations | Secondary \[A\] | VALID |
| E016 | Implement AI disclosure mechanisms | Secondary | DISCLOSE |
| F001 | Prevent AI cyber misuse | Secondary | PREV |
| F002 | Prevent catastrophic misuse | Secondary | DETECT |