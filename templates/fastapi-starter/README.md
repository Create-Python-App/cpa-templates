# FastAPI Starter

Production-oriented FastAPI API starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), and [pytest](https://docs.pytest.org/).

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
| `uv run pytest` | Run tests |

## Project layout

```
app/
  core/       # Settings and shared infrastructure
  api/v1/     # Versioned HTTP routes
tests/        # pytest suite
```

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.
