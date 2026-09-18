# Configuration

## Tooling (workspace root)

Shared Ruff / Pyright / mypy / pytest live in the root `pyproject.toml` and apply
across members unless a member overrides.

| Concern | Where |
|---------|--------|
| Python version | root `requires-python` / `.python-version` |
| Lint | `[tool.ruff]` at root |
| Types | `[tool.pyright]` + `[tool.mypy]` at root |
| Tests | `[tool.pytest.ini_options]` + member `tests/` |

## Member env

Apps that need secrets should ship their own `.env.example` and load via
pydantic-settings or `python-dotenv` inside that member — keep env local to the
deployable, not the shared library.

## Compatible extensions

- `github-setup`, `development-container`
- Prefer stack-specific Docker overlays only when an `apps/*` member matches
  (`fastapi-docker`, `django-docker`, `celery-docker`).
