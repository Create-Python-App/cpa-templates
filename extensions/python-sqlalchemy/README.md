# SQLAlchemy + Alembic (extension bank)

Maintainer-facing notes for the **python-sqlalchemy** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sqlalchemy` + `alembic` into project dependencies |
| `app/db/` | Engine, session factory, declarative `Base` |
| `alembic.ini` + `alembic/` | Migration environment |
| `.env.example.append` | Documents `DATABASE_URL` |
| `docs/SQLALCHEMY_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-sqlalchemy \
  --yes
```

Often combined with `python-postgres`:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-postgres python-sqlalchemy \
  --yes
```

## Verify after scaffold

```sh
uv sync
export DATABASE_URL=sqlite:///./app.db
uv run python -c "from app.db import get_db, session_factory"
uv run alembic current
```

See `template/docs/SQLALCHEMY_GUIDE.md` for full usage, configuration, and troubleshooting.
