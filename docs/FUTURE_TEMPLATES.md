# Future Templates

Growth backlog for templates and extensions. Prefer opening a tracking issue
before implementing anything listed under **Candidates**.

## Shipped

| Slug | Type | Notes |
|------|------|-------|
| `fastapi-starter` | `fastapi-backend` | Feature-based FastAPI starter (docs + Jinja options) |
| `cli-starter` | `cli-app` | Typer CLI with uv, Ruff, pytest, packaging entry points (`#37`) |
| `celery-worker` | `celery-worker` | Celery worker + beat skeleton (`#37`) |
| `django-api` | `django-backend` | Django API starter (`#50`) |
| `uv-workspace-starter` | `uv-workspace` | uv workspaces monorepo (`#55`) |

Compatible cross-cutting extensions use the `all-*` taxonomy
(`github-setup` → `extensions/all-github-setup`, etc.). Stack-specific addons
live under `fastapi-*`, `django-*`, and `celery-*`.

## Candidates

None currently tracked. Propose new starters via GitHub issues and follow
[AUTHORING.md](./AUTHORING.md).

## Contributing

Before implementing a new template:

1. Read [AUTHORING.md](./AUTHORING.md) and scaffold locally with `file://` URLs.
2. Propose the `type` string and compatible extensions in an issue.
3. Add the registry entry to `templates.json` only when the template passes CI
   smoke tests in [TESTING.md](./TESTING.md).
