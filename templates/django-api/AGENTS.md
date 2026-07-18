# AGENTS.md – AI Interaction & Execution Guide (Humans: see CONTRIBUTING.md & docs/)

## Authoritative references

| Topic | Source |
|-------|--------|
| Architecture | docs/PROJECT_STRUCTURE.md |
| API | docs/API.md |
| Testing | docs/TESTING_GUIDE.md |
| Deployment | docs/DEPLOYMENT.md |
| Configuration | docs/CONFIGURATION.md |
| Typing | docs/TYPING.md |

## Key commands

| Command | Purpose |
|---------|---------|
| `uv run python manage.py runserver` | Dev server |
| `uv run gunicorn config.wsgi:application` | Prod-style WSGI |
| `uv run ruff check .` | Lint |
| `uv run pytest` | Tests |
| `uv run mypy apps config` | Types |

## Feature work protocol

1. Copy `docs/examples/feature-app/` → `apps/<feature>/`.
2. Register in `INSTALLED_APPS`.
3. Wire urls under `API_PREFIX`.
4. Add tests; keep response envelope `{data,error,meta}`.
5. Update OpenAPI-facing serializers when shapes change (`/api/.../docs/`).
