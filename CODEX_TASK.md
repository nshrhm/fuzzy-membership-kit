# Coding-agent task brief

Maintain this repository as a reviewer-facing Python package for auditable fuzzy membership-function definitions.

## Guardrails

- Do not change a formula without updating both `docs/theory.md` and `docs/theory_ja.md`.
- Do not add a membership function without registering it in `FUNCTIONS` and adding unit tests.
- Keep configuration examples deterministic and small.
- Keep public APIs NumPy-friendly and scalar-friendly.
- Avoid hidden dependencies; update `pyproject.toml` when a dependency is necessary.

## Typical maintenance commands

```bash
uv sync --extra dev --extra plot --extra docs
uv run pytest
uv run ruff check src tests
uv run mkdocs build
```

## Next development targets

1. Add derivative functions for analytic smoothness checks.
2. Add CSV export for evaluated memberships.
3. Add a manifest generator that records config SHA-256 and git commit.
4. Add manuscript templates for Japanese and English fuzzy-systems venues.
