# PostgreSQL Guide

## Overview

The **python-postgres** extension adds a local Postgres 16 Compose service under `docker/postgres/`, merges the `psycopg[binary]` driver into `pyproject.toml`, and appends Postgres-related keys to `.env.example`.

It ships the **database service and client library** — wire your ORM and migrations in application code after scaffold.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `psycopg[binary]>=3.2` into project dependencies |
| `.env.example.append` | Appends Postgres keys to root `.env.example` |
| `docker/postgres/compose.yml` | Postgres 16 Alpine + volume + `pg_isready` healthcheck |
| `docker/postgres/.env.example` | Standalone env reference for the DB compose file |

## Usage

### Postgres only

```sh
docker compose -f docker/postgres/compose.yml up -d
```

Connect from the host:

```sh
psql "postgresql://app:app@localhost:5432/app"
```

### With python-docker

```sh
docker compose -f compose.yml -f docker/postgres/compose.yml up --build
```

The postgres compose file declares:

- `db` — Postgres 16 with a named volume and healthcheck
- `api` — `depends_on` with `condition: service_healthy` and `DATABASE_URL` injected

### Local development without Docker

```sh
uv sync
```

Install and run Postgres on the host (or use a cloud instance), then set `DATABASE_URL` in `.env`.

## Configuration

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `POSTGRES_USER` | `app` | DB user for local dev |
| `POSTGRES_PASSWORD` | `app` | Change in production |
| `POSTGRES_DB` | `app` | Database name |
| `DATABASE_URL` | (commented example) | e.g. `postgresql+psycopg://app:app@localhost:5432/app` |

When combined with **python-docker**, the postgres compose overlay sets:

```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
```

Use host `db` (Docker service name) inside compose; use `localhost` when connecting from the host machine.

## Verification

1. **Postgres only:** `docker compose -f docker/postgres/compose.yml up -d` — `db` reaches healthy.
2. **Healthcheck:** `docker compose -f docker/postgres/compose.yml ps` shows `healthy` for `db`.
3. **Connect:** `psql postgresql://app:app@localhost:5432/app -c 'SELECT 1'`.
4. **With API:** After full stack compose, `curl -s http://localhost:8000/api/v1/healthz` still returns OK (API does not require DB until you wire it).
5. **Dependency:** `uv run python -c "import psycopg"` succeeds after `uv sync`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `connection refused` on localhost:5432 | Compose not running | Start `docker/postgres/compose.yml` |
| Auth failure | Wrong user/password/db | Match `POSTGRES_*` in `.env` |
| App cannot reach DB in Docker | Using `localhost` as host inside API container | Use hostname `db` |
| Volume has stale data | Old volume after credential change | `docker compose -f docker/postgres/compose.yml down -v` (destroys data) |
| `import psycopg` fails | Overlay not merged / sync skipped | Confirm `pyproject.toml` deps and re-run `uv sync` |

## Resources

- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [psycopg 3 docs](https://www.psycopg.org/psycopg3/docs/)
- [Compose multiple files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)
