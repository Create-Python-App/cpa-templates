# PostgreSQL

Postgres Compose service under `docker/postgres/` — same layout pattern as cna-templates DB extensions (`docker/<engine>/compose.yml`).

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

Copy `docker/postgres/.env.example` values into your root `.env` (or extend it):

```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=app
```

## Local development without Docker

```sh
uv add "psycopg[binary]"
```

Wire SQLAlchemy or your ORM in the application layer when you add persistence.
