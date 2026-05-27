# Conventions

- Code uses `from __future__ import annotations` and strict type hints.
- Indentation style is tabs (`ruff.toml`). Quote style is single quotes where linted.
- Project naming often uses camelCase for functions, fixtures, variables, and test helper names.
- Test helpers and shared fixtures live in `tests/conftest.py`; tests commonly import `uniformTestFailureMessage`, `prototype_numpyAllClose`, or `prototype_numpyArrayEqual` from there.
- Pytest tests should be parametrized; fixtures belong in `tests/conftest.py`.