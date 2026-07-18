# AGENTS.md – AI Interaction & Execution Guide (Humans: see CONTRIBUTING.md & docs/)

## Authoritative references

| Topic | Source |
|-------|--------|
| Architecture | docs/PROJECT_STRUCTURE.md |
| Configuration | docs/CONFIGURATION.md |
| Testing | docs/TESTING_GUIDE.md |
| Deployment | docs/DEPLOYMENT.md |
| Typing | docs/TYPING.md |

## Key commands

| Command | Purpose |
|---------|---------|
| `uv run celery -A worker.celery_app worker --loglevel=INFO` | Run worker |
| `uv run pytest` | Eager-mode tests |
| `uv run ruff check .` | Lint |
| `uv run mypy worker` | Types |

## Task work protocol

1. Add modules under `worker/tasks/<domain>.py`.
2. Export from `worker/tasks/__init__.py` when callers import by name.
3. Keep task names stable (`worker.tasks.<name>`).
4. Cover with eager pytest; do not require Redis in unit tests.
5. Update docs when introducing retries, routing, or beat schedules.

## Guardrails

- Do not put business logic only inside `@app.task` wrappers without a testable function body.
- Do not hardcode broker URLs in code — use settings / env.
- Flag large dependency additions for human confirmation.
