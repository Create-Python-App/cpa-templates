# Django API

Django + Django REST Framework API starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), and [pytest-django](https://pytest-django.readthedocs.io/).

## Quick start

```sh
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run python manage.py runserver` | Start dev server |
| `uv run python manage.py migrate` | Apply migrations |
| `uv run ruff check .` | Lint |
| `uv run pytest` | Run tests |

## Health probes

| Endpoint | Purpose |
|----------|---------|
| `GET /ping/` | Minimal probe |
| `GET {apiPrefix}/healthz` | API readiness probe |

## Compatible extensions

| Slug | Notes |
|------|-------|
| `github-setup` | CI / Dependabot |
| `python-devcontainer` | VS Code Dev Container |
| `python-postgres` | Postgres Compose + driver (wire `DATABASES` manually) |

`python-docker` currently targets FastAPI (`uvicorn app.main:app`) and is not compatible yet.

## Configuration

Copy `.env.example` to `.env`. Scaffold option:

| Option | Default | Description |
|--------|---------|-------------|
| `apiPrefix` | `/api/v1` | Prefix for API routes including `/healthz` |
