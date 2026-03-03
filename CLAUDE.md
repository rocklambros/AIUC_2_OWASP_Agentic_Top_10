# AIUC 2 - OWASP Agentic Top 10

## Project Context
Python + JSON project analyzing the OWASP Top 10 for Agentic Applications (2026).

## Conventions
- Python 3.12+, strict typing with mypy
- Linting: ruff (E, F, I, N, W, UP rules)
- Tests in `tests/` using pytest
- Line length: 100 chars
- OWASP reference data in `owasp/` directory (read-only JSON)
- Core code in `aiuc/` package

## Key Files
- `owasp/2025-OWASP-Top-10-for-Agentic-Applications-2026-12.6-1-FINAL.json` — Full OWASP dataset
- `aiuc/` — Main Python package
- `pyproject.toml` — Project configuration

## Security Rules
Security coding rules from [TikiTribe/claude-secure-coding-rules](https://github.com/TikiTribe/claude-secure-coding-rules) are installed in `.claude/rules/`:

| Rule File | Scope | Standards Covered |
|-----------|-------|-------------------|
| `python-security.md` | Python language security | CWE-22, CWE-78, CWE-89, CWE-330, CWE-502, CWE-918 |
| `ai-security.md` | AI/ML system security | NIST AI RMF, MITRE ATLAS, ISO/IEC 23894, Google SAIF |
| `agent-security.md` | Agentic AI security | OWASP LLM Top 10, tool validation, permission boundaries |
| `owasp-2025.md` | Web application security | OWASP Top 10:2025 (A01-A10) |

### Enforcement Levels
- **strict**: Never generate violating code (SQL injection, command injection, unsafe deserialization)
- **warning**: Warn and suggest alternatives (missing input validation, weak crypto)
- **advisory**: Mention as best practice (security headers, rate limiting)
