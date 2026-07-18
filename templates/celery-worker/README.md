# Celery Worker

Celery worker starter with Redis broker defaults, feature-style task modules,
[uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), and
[pytest](https://docs.pytest.org/).

## Quick start

```sh
# Start Redis locally (example)
docker run --rm -p 6379:6379 redis:7

cp .env.example .env
uv sync
uv run celery -A worker.celery_app worker --loglevel=INFO
```

In another shell:

```sh
uv run python -c "from worker.tasks import ping; print(ping.delay().get(timeout=5))"
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run celery -A worker.celery_app worker --loglevel=INFO` | Run worker |
| `uv run celery -A worker.celery_app beat --loglevel=INFO` | Run beat (when schedules are added) |
| `uv run ruff check .` | Lint |
| `uv run pytest` | Eager-mode unit tests (no broker) |

## Project layout

```
worker/
  celery_app.py   # Celery app
  config.py       # pydantic-settings
  tasks/          # task modules (health, math, …)
tests/            # eager-mode pytest suite
docs/             # structure, config, testing, deployment
```

## Configuration

Copy `.env.example` to `.env`. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

Scaffold-time options:

| Option | Default | Description |
|--------|---------|-------------|
| `brokerUrl` | `redis://localhost:6379/0` | Celery broker |
| `resultBackend` | `redis://localhost:6379/1` | Result backend |

Compatible extensions: `celery-docker`, `postgres`, `github-setup`, `development-container`.

## Docs

- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [AGENTS.md](AGENTS.md) · [CONTRIBUTING.md](CONTRIBUTING.md)
