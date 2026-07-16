# GitHub Setup

This extension adds GitHub Actions CI, Dependabot, and community health files.

## CI

The `ci.yml` workflow runs on push/PR to `main`:

- `uv sync`
- `uv run ruff check .`
- `uv run pytest`

Customize steps in `.github/workflows/ci.yml` as your project grows.
