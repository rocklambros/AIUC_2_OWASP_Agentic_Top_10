# AIUC 2 - OWASP Agentic Top 10

## Overview
Analysis and implementation project for the OWASP Top 10 for Agentic Applications (2026).

## Tech Stack
- **Language**: Python 3.12
- **Data Format**: JSON
- **Testing**: pytest
- **Linting**: ruff, mypy

## Structure
```
aiuc/               # Core Python package
owasp/              # OWASP reference data (JSON)
tests/              # Test suite
.zerg/              # ZERG configuration
.gsd/               # Project documentation
```

## OWASP Agentic Top 10 Entries
1. ASI01 - Agent Goal Hijack
2. ASI02 - Tool Misuse and Exploitation
3. ASI03 - Identity & Privilege Abuse
4. ASI04 - Agentic Supply Chain Vulnerabilities
5. ASI05 - Unexpected Code Execution
6. ASI06 - Memory & Context Poisoning
7. ASI07 - Multi-Agent Trust Issues
8. ASI08 - Insufficient Monitoring & Logging
9. ASI09 - Lack of Human Oversight
10. ASI10 - Rogue Agents

## Commands
```bash
# Run tests
pytest

# Lint
ruff check .
mypy aiuc/
```
