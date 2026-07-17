# SQLAlchemy + Alembic

Adds SQLAlchemy 2.x session helpers and an Alembic migration layout for FastAPI starters.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sqlalchemy` + `alembic` |
| `app/db/` | Engine, session factory, declarative `Base` |
| `alembic.ini` + `alembic/` | Migration environment |
| `.env.example.append` | Documents `DATABASE_URL` |

## Quick start

```sh
uv sync
# optional: pair with python-postgres
export DATABASE_URL=sqlite:///./app.db
uv run alembic revision -m "init" --autogenerate
uv run alembic upgrade head
```

Use `Depends(get_db)` in routers after importing from `app.db`.

## Verification

1. `uv run python -c "from app.db import get_db, session_factory"`
2. `uv run alembic current`
