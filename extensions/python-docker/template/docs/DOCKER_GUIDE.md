# Docker Guide

## Overview

The **python-docker** extension adds a reproducible container workflow for FastAPI (or other uv-based Python API) projects. Compose files follow Create-Node-App naming: **`compose.yml`** / **`compose.prod.yml`** (not `docker-compose.yml`).

Use it when you want local containers without installing Python on the host, or when you ship the API as an image. Pair with **python-postgres** when you need a database service.

## What it adds

| Path | Purpose |
|------|---------|
| `Dockerfile` | Image based on `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` |
| `.dockerignore` | Keeps `.venv`, caches, and git metadata out of the build context |
| `compose.yml` | Dev: bind-mount source, `--reload`, port `8000` |
| `compose.prod.yml` | Prod overlay: no bind mount, `restart: always`, no reload |

## Usage

### Development

```sh
docker compose up --build
```

- OpenAPI docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/healthz (default `API_PREFIX=/api/v1`)

The dev compose file bind-mounts the project directory and runs uvicorn with `--reload`.

### Production-style run

```sh
docker compose -f compose.yml -f compose.prod.yml up --build -d
```

The prod overlay removes the source bind mount and `--reload`, and sets `restart: always`.

### With python-postgres

```sh
docker compose -f compose.yml -f docker/postgres/compose.yml up --build
```

## Configuration

Create `.env` at the project root (copy from `.env.example` after scaffold). Common keys from `fastapi-starter`:

| Variable | Default | Notes |
|----------|---------|-------|
| `DEBUG` | `false` | Prefer `true` only for local non-Docker debugging |
| `HOST` | `127.0.0.1` | Compose uses uvicorn `--host 0.0.0.0` |
| `PORT` | `8000` | Mapped in `compose.yml` |
| `API_PREFIX` | `/api/v1` | From template scaffold options |
| `CORS_ORIGINS` | localhost URLs | Comma-separated when used by the app |

For production-style runs, set `DEBUG=false` in `.env`. Pin base image tags in `Dockerfile` for reproducible builds.

## Verification

1. **Build:** `docker compose build` completes without errors.
2. **Start:** `docker compose up --build` — container stays running.
3. **Health:** `curl -s http://localhost:8000/api/v1/healthz` returns an `APIResponse` with `"dev_code":"HEALTH_OK"`.
4. **Docs:** Open http://localhost:8000/docs.
5. **Prod overlay:** `docker compose -f compose.yml -f compose.prod.yml config` validates merged config.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Port 8000 already allocated | Host process or another compose stack | Stop the other service or change the published port |
| Module not found inside container | Image built without latest `pyproject.toml` | Rebuild: `docker compose build --no-cache` |
| Health 404 | Wrong prefix | Check `API_PREFIX` / scaffold `apiPrefix` (default `/api/v1/healthz`) |
| Env vars missing | No `.env` | Copy `.env.example` → `.env` |
| Postgres hostname errors | Using `localhost` inside compose | Use service name `db` when stacked with `python-postgres` |

## Resources

- [Docker Compose V2](https://docs.docker.com/compose/)
- [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/)
- [FastAPI deployment](https://fastapi.tiangolo.com/deployment/)
- Project [Deployment](./DEPLOYMENT.md) doc (from the base template)
