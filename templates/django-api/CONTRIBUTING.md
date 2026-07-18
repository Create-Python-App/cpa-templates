# Contributing

## Setup

```bash
uv sync
uv run python manage.py migrate
uv run pytest
```

## Style

- Feature apps under `apps/`
- Copy new features from `docs/examples/feature-app/`
- Ruff for lint/format
- Typed public APIs (serializers + view annotations)

## Docs

Update the matching file under `docs/` when behaviour changes. Keep `AGENTS.md` as a pointer table, not a second docs tree.

## Extensions

Optional: `django-docker`, `postgres`, `github-setup`, `development-container`.
