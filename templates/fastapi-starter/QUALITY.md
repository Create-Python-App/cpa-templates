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

This starter does not ship an ORM by default. When using the `fastapi-sqlalchemy`
and/or `postgres` extensions:

```sh
uv run alembic upgrade head   # after adding fastapi-sqlalchemy
```

## Extension slots (catalog slugs)

| Slug | Role |
|------|------|
| `fastapi-docker` | Dockerfile + Compose |
| `postgres` | Postgres Compose + `psycopg` |
| `development-container` | VS Code Dev Container |
| `github-setup` | GitHub Actions / Dependabot / templates |

Example:

```sh
uvx create-awesome-python-app@latest my-api \
  --template fastapi-starter \
  --addons fastapi-docker \
  --addons postgres \
  --addons development-container \
  --no-interactive
```

