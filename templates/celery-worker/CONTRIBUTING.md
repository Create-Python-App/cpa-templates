# Contributing

## Setup

```bash
uv sync
uv run pytest
```

Optional local broker:

```bash
docker run --rm -p 6379:6379 redis:7
uv run celery -A worker.celery_app worker --loglevel=INFO
```

## Style

- Task modules under `worker/tasks/`
- Ruff for lint/format
- Typed public task signatures

## Docs

Update the matching file under `docs/` when behaviour changes. Keep `AGENTS.md`
as a pointer table, not a second docs tree.

## Extensions

Optional: `celery-docker`, `postgres`, `github-setup`, `development-container`.
