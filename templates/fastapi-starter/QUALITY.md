# Template quality checklist (M1)

Use this checklist before calling a FastAPI starter "mature" for CPA.

## Required

- [x] README documents run / lint / test (and typecheck when applicable)
- [x] Health probes exist: `GET /ping` and `GET {apiPrefix}/healthz`
- [x] Health covered by pytest smoke tests
- [x] `.env.example` documents settings used by `app.core.config`
- [x] `uv sync` + `uv run ruff check .` + `uv run pytest` pass after scaffold
- [x] Compatible extensions documented with real catalog slugs
- [x] Docs suite present (`PROJECT_STRUCTURE`, `API`, `TESTING_GUIDE`, `DEPLOYMENT`)

## Typing (default)

- [x] `mypy` and `pyright` in the dev dependency group
- [x] `[tool.mypy]` and `[tool.pyright]` configured in `pyproject.toml`
- [x] README documents `uv run mypy app` and `uv run pyright`

## Migrations

This starter does not ship an ORM by default. When using the `python-sqlalchemy`
and/or `python-postgres` extensions:

```sh
uv run alembic upgrade head   # after adding python-sqlalchemy
```

## Extension slots (catalog slugs)

| Slug | Role |
|------|------|
| `python-docker` | Dockerfile + Compose |
| `python-postgres` | Postgres Compose + `psycopg` |
| `python-devcontainer` | VS Code Dev Container |
| `github-setup` | GitHub Actions / Dependabot / templates |

Example:

```sh
uvx create-awesome-python-app@latest my-api \
  --template fastapi-starter \
  --addons python-docker \
  --addons python-postgres \
  --addons python-devcontainer \
  --no-interactive
```

