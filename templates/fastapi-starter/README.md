# FastAPI Starter

Production-oriented FastAPI API starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [pytest](https://docs.pytest.org/), [mypy](https://mypy.readthedocs.io/), and [pyright](https://github.com/microsoft/pyright).

## Quick start

```sh
uv sync
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Commands

| Command | Description |
|---------|-------------|
| `uv run uvicorn app.main:app --reload` | Start dev server |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run mypy app` | Type-check with mypy |
| `uv run pyright` | Type-check with pyright |
| `uv run pytest` | Run tests |

## Project layout

```
app/
  api/        # API router composition
  core/       # Settings, middleware, logging, exception handlers
  features/   # Feature-based modules (router/service/schemas)
  schemas/    # Shared response/request schemas
tests/        # pytest suite
```

See the docs suite for deeper guidance:

- [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md) — feature-based architecture
- [`docs/API.md`](docs/API.md) — endpoints and response envelope
- [`docs/TESTING_GUIDE.md`](docs/TESTING_GUIDE.md) — pytest patterns
- [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) — shipping and health probes
- [`docs/README.md`](docs/README.md) — docs index

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

The template also exposes scaffold-time options through `cpa.config.json`:

| Option | Default | Description |
|--------|---------|-------------|
| `apiPrefix` | `/api/v1` | Prefix used when mounting `app/api/router.py` |
| `enableCors` | `true` | Whether generated `app/main.py` registers CORS middleware |
