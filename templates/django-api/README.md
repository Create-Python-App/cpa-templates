# Django + DRF API

Production-oriented Django REST Framework starter with a **feature-app** layout,
uv, Ruff, pytest-django, mypy/pyright stubs, and docs that match the CPA quality bar.

## Quickstart

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
curl -s http://127.0.0.1:8000/api/v1/healthz/
# OpenAPI UI: http://127.0.0.1:8000/api/v1/docs/
```

Tests and lint:

```bash
uv run pytest
uv run ruff check .
uv run mypy apps config
```

## Architecture

Domain code lives under `apps/<feature>/` (serializers, services, views, urls).
Project wiring lives under `config/`. Copy `docs/examples/feature-app/` when adding a feature.

See [docs/PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md).

## Documentation

| Doc | Topic |
|-----|-------|
| [docs/README.md](./docs/README.md) | Index |
| [docs/API.md](./docs/API.md) | Endpoints, envelope, OpenAPI |
| [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) | Env and tooling |
| [docs/TESTING_GUIDE.md](./docs/TESTING_GUIDE.md) | pytest-django |
| [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) | Containers and prod |
| [docs/TYPING.md](./docs/TYPING.md) | mypy / pyright |
| [AGENTS.md](./AGENTS.md) | AI assistant guide |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Human contributor guide |

## Compatible extensions

| Slug | Purpose |
|------|---------|
| `github-setup` | CI / Dependabot / PR automation |
| `development-container` | VS Code Dev Container |
| `django-docker` | Dockerfile + Compose for Django |
| `postgres` | Postgres Compose service (wire `DATABASES` / URL) |
