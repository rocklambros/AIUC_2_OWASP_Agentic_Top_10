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
