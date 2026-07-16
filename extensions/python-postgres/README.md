# PostgreSQL overlay

Use with the `python-docker` extension (or any compose-based setup).

## Quick start

```sh
# Start API + Postgres
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up --build
```

Set in `.env`:

```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
```

## Local development without Docker

Install a driver and point `DATABASE_URL` at your instance:

```sh
uv add psycopg[binary]
```

Wire SQLAlchemy or your ORM in the application layer when you add persistence.
