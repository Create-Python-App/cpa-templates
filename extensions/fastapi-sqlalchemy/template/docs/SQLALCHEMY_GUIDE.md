# SQLAlchemy Guide

## Overview

The **fastapi-sqlalchemy** extension adds SQLAlchemy 2.x session helpers and an Alembic migration layout for FastAPI starters. It merges `sqlalchemy` and `alembic` into `pyproject.toml` and documents `DATABASE_URL` in `.env.example`.

Pair with **postgres** when you want a local Postgres Compose service and the `psycopg` driver; the default URL is SQLite for smoke tests without Docker.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sqlalchemy>=2.0.36` and `alembic>=1.14.0` |
| `app/db/base.py` | Declarative `Base` for ORM models |
| `app/db/session.py` | Engine, `session_factory`, and `get_db()` dependency |
| `app/db/__init__.py` | Re-exports `get_db` and `session_factory` |
| `alembic.ini` + `alembic/` | Migration environment wired to `Base.metadata` |
| `.env.example.append` | Documents `DATABASE_URL` |

## Usage

### Local smoke (SQLite)

```sh
uv sync
export DATABASE_URL=sqlite:///./app.db
uv run alembic revision -m "init" --autogenerate
uv run alembic upgrade head
```

### FastAPI dependency

```python
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db


@router.get("/items")
def list_items(db: Session = Depends(get_db)) -> list[dict]:
    ...
```

### With postgres

```sh
docker compose -f docker/postgres/compose.yml up -d
# Set DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app in .env
uv sync
uv run alembic upgrade head
```

## Configuration

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `DATABASE_URL` | (commented) | e.g. `sqlite:///./app.db` or `postgresql+psycopg://app:app@localhost:5432/app` |

`app/db/session.py` falls back to `sqlite:///./app.db` when `DATABASE_URL` is unset. SQLite enables `check_same_thread=False` for FastAPI sync sessions.

Alembic reads `DATABASE_URL` from the environment when set; otherwise it uses `sqlalchemy.url` from `alembic.ini`.

## Verification

1. `uv run python -c "from app.db import get_db, session_factory"` succeeds after `uv sync`.
2. `uv run alembic current` runs without error (empty DB is fine).
3. After adding a model on `Base`, `uv run alembic revision -m "init" --autogenerate` produces a revision under `alembic/versions/`.
4. `uv run alembic upgrade head` applies migrations.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No module named 'app.db'` | Package not installed / wrong cwd | Run from project root after `uv sync` |
| Autogenerate empty | Models not imported in env | Import model modules in `alembic/env.py` (or a models package) so they register on `Base.metadata` |
| Postgres connection refused | DB not running / wrong host | Start `docker/postgres/compose.yml`; use `localhost` from host, `db` inside Compose |
| SQLite lock errors | Concurrent writers | Use Postgres for multi-worker setups |
| Typing noise on layered typed starter | Rare stub gaps | SQLAlchemy 2.x ships typing; keep public APIs annotated |

## Resources

- [SQLAlchemy 2.0 documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [FastAPI SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
