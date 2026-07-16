# PostgreSQL

Postgres Compose service under `docker/postgres/` — same layout pattern as cna-templates DB extensions (`docker/<engine>/compose.yml`).

This extension also merges a partial `pyproject.toml` that adds `psycopg[binary]`, and appends Postgres env vars via `.env.example.append`.

## Quick start (Postgres only)

```sh
docker compose -f docker/postgres/compose.yml up -d
```

## With the `python-docker` extension

From the project root (after both extensions are applied):

```sh
# API (compose.yml) + Postgres (docker/postgres/compose.yml)
docker compose -f compose.yml -f docker/postgres/compose.yml up --build
```

Root `.env.example` gains Postgres keys from `.env.example.append`. Typical values:

```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=app
```

## Local development without Docker

`psycopg` is added automatically via the merged `pyproject.toml`. Wire SQLAlchemy or your ORM when you add persistence.
