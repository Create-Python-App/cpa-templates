# Future Templates

Planned templates and extensions not yet in `templates.json`. These are phased additions — see open issues in [Create-Python-App/cpa-templates](https://github.com/Create-Python-App/cpa-templates/issues).

## Recently shipped

| Slug | Type | Description |
|------|------|-------------|
| `uv-workspace-starter` | `uv-workspace` | Python monorepo using uv workspaces: shared `packages/` libraries and `apps/` deployables with one lockfile, shared Ruff/Pyright/pytest, and a Typer CLI that consumes a local library. Compatible extensions: `github-setup`, `python-devcontainer`. |

## Planned templates

| Slug | Type (proposed) | Description | Phase |
|------|-----------------|-------------|-------|
| `cli-starter` | `cli-app` | Typer or Click CLI with uv, Ruff, pytest, and packaging entry points | 1 |
| `celery-worker` | `celery-worker` | Celery worker + beat skeleton with Redis/RabbitMQ hooks and Docker compose overlay | 2 |

### `cli-starter`

- **When:** Command-line tools, internal utilities, or libraries shipped as console scripts.
- **Stack:** `pyproject.toml` with `[project.scripts]`, Typer (or Click), pytest for CLI invocation tests.
- **Extensions:** `github-setup`, `python-devcontainer`; Docker extension optional for containerized CLI distribution.

### `celery-worker`

- **When:** Background jobs, scheduled tasks, or async processing separate from an HTTP API.
- **Stack:** Celery app module, worker/beat commands, health probe, example task.
- **Extensions:** `python-docker`, `python-postgres` (for result backend or ORM), message-broker compose under `docker/redis/` or similar.

## Contributing

Before implementing a new template:

1. Read [AUTHORING.md](./AUTHORING.md) and scaffold locally with `file://` URLs.
2. Propose the `type` string and compatible extensions in an issue.
3. Add the registry entry to `templates.json` only when the template passes CI smoke tests in [TESTING.md](./TESTING.md).
