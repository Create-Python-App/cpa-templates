# Flower guide (Celery)

## Overview

The **flower-docker** extension packages the Celery worker with a **Flower**
monitoring dashboard for local and production-style containers. It includes a
Redis broker, a worker, and a Flower service.

Use it when you want real-time task monitoring (`http://localhost:5555`) without
installing Flower on the host. It is mutually exclusive with `celery-docker`
(both ship `Dockerfile` / `compose.yml` for `celery-worker`).

## What it adds

| Path | Purpose |
|------|---------|
| `Dockerfile` | Image based on `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` |
| `.dockerignore` | Keeps `.venv`, caches, and git metadata out of the build context |
| `compose.yml` | Dev: `redis` + `worker` + `flower` (port 5555) with healthchecks |
| `compose.prod.yml` | Prod overlay: `restart: always`, `--concurrency=2`, healthchecks |
| `pyproject.toml` | Merges `flower>=2.0.1` into project dependencies |
| `.env.example` / `.env.example.append` | Flower env examples (`FLOWER_BASIC_AUTH`, `FLOWER_PORT`) |

Env overrides in Compose: `BROKER_URL` / `RESULT_BACKEND` point at the
`redis` service (not `localhost`). These names match `worker/config.py`
(pydantic-settings fields `broker_url` / `result_backend`).

## Usage

### Development

```sh
docker compose up --build
```

- Flower dashboard: http://localhost:5555
- Redis: localhost:6379

The dev compose file bind-mounts the project directory for the worker.

### Production-style run

```sh
docker compose -f compose.yml -f compose.prod.yml up --build -d
```

The prod overlay removes `--reload` concerns, sets `restart: always`, and
uses `--concurrency=2` for the worker.

### With basic auth (recommended for non-local)

1. Set in `.env`:

```env
FLOWER_BASIC_AUTH=user:password
```

2. Restart: `docker compose up --build`
3. Open http://localhost:5555 — browser prompts for user/password.

Flower can expose task arguments and results. Never commit `.env` to version
control; add `.env` to `.gitignore`. In production, place Flower behind a
reverse proxy with TLS.

## Configuration

Create `.env` at the project root (copy from `.env.example` after scaffold).

| Variable | Default | Notes |
|----------|---------|-------|
| `BROKER_URL` | `redis://redis:6379/0` | Broker for worker + flower (Compose overrides to service name) |
| `RESULT_BACKEND` | `redis://redis:6379/1` | Result backend |
| `FLOWER_BASIC_AUTH` | (unset) | `user:password` for HTTP basic auth; leave unset for local dev |
| `FLOWER_PORT` | `5555` | Flower listen port (Compose maps `5555:5555`) |

For the worker, `BROKER_URL` / `RESULT_BACKEND` are read via `worker/config.py`.
Flower reuses the same broker env (`--broker` defaults to `BROKER_URL`).

## Verification

1. `docker compose up --build`
2. Confirm Redis is healthy: `docker compose ps` shows `healthy` for `redis`
3. Confirm worker is ready: log shows `celery@... ready`
4. Confirm Flower is healthy: `docker compose ps` shows `healthy` for `flower` and log shows `Visit me at http://0.0.0.0:5555`
5. Open http://localhost:5555 — dashboard lists workers and tasks
6. Enqueue a task:

```sh
docker compose exec worker uv run python -c \
  "from worker.tasks import ping; print(ping.delay().get(timeout=10))"
```

Flower should show the task in the dashboard.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Cannot connect to Redis | Use `redis://redis:6379/0` inside Compose (service name), not `localhost` |
| Flower not reachable on 5555 | Check `docker compose ps`; flower healthcheck may still be starting (10s start period) |
| Worker not appearing in Flower | Ensure `BROKER_URL` matches for both services; restart `docker compose up --build` |
| Flower asks for password unexpectedly | Unset `FLOWER_BASIC_AUTH` in `.env` for local dev, or provide `user:password` correctly |
| Import errors for `worker` | Confirm `COPY worker` matches the template layout |
| `flower` command fails | Confirm `flower` is installed: `uv run python -c "import flower"` after `uv sync` |

## Resources

- [Flower docs](https://flower.readthedocs.io/)
- [Celery first steps](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
- [Celery monitoring and management guide](https://docs.celeryq.dev/en/stable/userguide/monitoring.html)
