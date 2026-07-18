# FastAPI Starter

This project was generated using [create-awesome-python-app](https://pypi.org/project/create-awesome-python-app/). **DON'T USE THIS TEMPLATE AS IT!** Generate yours using the CLI and following the options in the interactive menu. Check the docs for more information!

Production-oriented FastAPI API starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [pytest](https://docs.pytest.org/), [mypy](https://mypy.readthedocs.io/), and [pyright](https://github.com/microsoft/pyright).

## Features

- ⚡ **FastAPI** — modern async ASGI API framework
- 🦾 **Typed Python** — Pydantic models plus mypy / pyright as the default quality bar
- 📦 **[uv](https://docs.astral.sh/uv/)** — fast installs and lockfile-friendly workflows
- 🧹 **[Ruff](https://docs.astral.sh/ruff/)** — lint and format in one tool
- ✅ **[pytest](https://docs.pytest.org/)** — API tests with FastAPI `TestClient`
- 🏗️ **Feature-Based Architecture** — scalable modules under `app/features/`
- 🔒 **Encapsulated Features** — router / service / schemas with clear boundaries
- 🎯 **Domain-Driven Layout** — structure reflects API capabilities, not frameworks

## Architecture

This template uses a Feature-Based Architecture inspired by Screaming Architecture and Domain-Driven Design principles (parity with Create-Node-App's `react-vite-starter`). The codebase is organized around API capabilities rather than technical layers alone:

- 📦 **Modular**: Each feature is self-contained
- 🔄 **Maintainable**: Changes stay isolated to a feature
- 🚀 **Scalable**: Add features without rewriting the app shell
- 🎨 **Clear**: Folders reflect business capabilities

For detailed information, see [Project Structure](./docs/PROJECT_STRUCTURE.md).

## Extra documentation

Useful guides for structure, API contracts, testing, typing, configuration, and deployment live in the [docs](./docs) folder.

## Pre-packed

### Dev tools

- [uv](https://docs.astral.sh/uv/) — package and environment management
- [Ruff](https://docs.astral.sh/ruff/) — linting and formatting
- [mypy](https://mypy-lang.org/) / [pyright](https://github.com/microsoft/pyright) — static typing (default)
- [pytest](https://docs.pytest.org/) — test runner
- [httpx](https://www.python-httpx.org/) — HTTP client for tests

## Quickstart

```sh
uv sync
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive OpenAPI docs.

## Development

While developing you will rely mostly on uvicorn with `--reload`. Additional commands:

| Command | Description |
|---------|-------------|
| `uv run uvicorn app.main:app --reload` | Serve the API for local development |
| `uv run ruff check .` | Lint with Ruff |
| `uv run ruff format .` | Format with Ruff |
| `uv run ruff format --check .` | Check formatting without writing |
| `uv run mypy app` | Static type check (mypy) |
| `uv run pyright` | Static type check (pyright) |
| `uv run pytest` | Run the test suite |

See [Configuration](./docs/CONFIGURATION.md) and [Typing](./docs/TYPING.md) for tool setup details.

## API

| Path | Purpose |
|------|---------|
| `{API_PREFIX}/healthz` | Health probe (`APIResponse` envelope) |
| `/docs` | Swagger UI (OpenAPI) |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI schema |

Default `API_PREFIX` is `/api/v1` (scaffold option `apiPrefix`). Details: [API.md](./docs/API.md).

## Production

Scripts and notes for shipping:

| Approach | Description |
|----------|-------------|
| `uv sync --frozen --no-dev` | Reproducible runtime install |
| `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` | Production-style ASGI process |
| Health probe | `GET {API_PREFIX}/healthz` → `dev_code: HEALTH_OK` |

Full guidance: [Deployment](./docs/DEPLOYMENT.md). Pair with the `fastapi-docker` / `postgres` extensions when you need containers or a database.

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

Scaffold-time options (`cpa.config.json`):

| Option | Default | Description |
|--------|---------|-------------|
| `apiPrefix` | `/api/v1` | Prefix when mounting `app/api/router.py` |
| `enableCors` | `true` | Whether generated `app/main.py` registers CORS middleware |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the local contribution workflow (bootstrap, architecture, commits, PR checklist). For overarching template issues or improvements, open issues / PRs in the upstream monorepo: [Create-Python-App/cpa-templates](https://github.com/Create-Python-App/cpa-templates).


## Health probes

| Endpoint | Purpose |
|----------|---------|
| `GET /ping` | Minimal load-balancer probe |
| `GET {apiPrefix}/healthz` | App readiness probe (tested in `tests/test_health.py`) |

## Compatible extensions

Use catalog slugs (not informal names like `docker` / `vscode`):

| Slug | Adds |
|------|------|
| `fastapi-docker` | Dockerfile + Compose |
| `postgres` | Postgres Compose + driver |
| `development-container` | VS Code Dev Container |
| `github-setup` | CI / Dependabot / issue templates |

Migrations are not bundled in the base starter. Add `fastapi-sqlalchemy` (and usually
`postgres`) when you need Alembic/`DATABASE_URL` workflows.

## Quality bar

See [`QUALITY.md`](QUALITY.md) for the M1 maturity checklist.
