# Deployment

This guide covers shipping a scaffolded `fastapi-starter` project. It mirrors
the operational depth expected in Create-Node-App starter docs, adapted for a
FastAPI + uv stack.

## Prerequisites

- Python version from `.python-version` / `requires-python` in `pyproject.toml`
- [uv](https://docs.astral.sh/uv/) available in CI and runtime images
- A process manager or platform that can run ASGI (Uvicorn / Gunicorn+Uvicorn)

## Build a release environment

```bash
uv sync --frozen --no-dev
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Use `--frozen` in CI/CD once a lockfile is committed so installs stay
reproducible.

## Environment variables

Copy `.env.example` to the platform secret store (never commit real secrets).

| Variable | Purpose |
|----------|---------|
| `API_PREFIX` | URL prefix for the composed API router (default `/api/v1`) |
| `ENABLE_CORS` | Toggle CORS middleware when settings read this flag |
| App-specific settings | Add in `app/core/config.py` and document here as you grow |

Production checklist:

1. Restrict CORS origins (do not ship wildcard origins to the public internet).
2. Set a stable log level and retain `X-Request-ID` propagation.
3. Expose `{API_PREFIX}/healthz` as the readiness/liveness probe.
4. Terminate TLS at the load balancer / ingress.

## Container sketch

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app ./app
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Health probe example:

```text
GET /api/v1/healthz
```

Expect HTTP `200` and `"dev_code": "HEALTH_OK"`.

## Platform notes

### Docker Compose

Pair this API with the `fastapi-docker` / `postgres` extensions when you
need local containers or a database. Keep the API service dependent on DB health
before accepting traffic.

### Kubernetes / Cloud Run / Fly.io

- Set CPU/memory based on expected concurrency; Uvicorn workers are processes.
- Configure rolling updates to wait on the healthz probe.
- Inject secrets through the platform — do not bake `.env` into images.

## Observability

- Request IDs from `RequestIDMiddleware` should appear in access logs and error
  envelopes.
- Prefer structured logging (`app/core/logging_config.py`) and forward to your
  log drain.
- Track 5xx rate and healthz latency as first SLOs.

## Rollback

1. Keep previous image tags immutable.
2. Roll back the deployment object / release to the last known-good tag.
3. Confirm `{API_PREFIX}/healthz` and a smoke request against a critical path.

## Related docs

- [`API.md`](./API.md) — envelope and health contract
- [`TESTING_GUIDE.md`](./TESTING_GUIDE.md) — pre-deploy verification
- [`CONFIGURATION.md`](./CONFIGURATION.md) — env and tooling
- [`PROJECT_STRUCTURE.md`](./PROJECT_STRUCTURE.md) — where to place new features
