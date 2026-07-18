# PostgreSQL (extension bank)

Maintainer-facing notes for the **postgres** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `psycopg[binary]` into project dependencies |
| `.env.example.append` | Appends Postgres keys to root `.env.example` |
| `docker/postgres/compose.yml` | Postgres 16 service + volume + healthcheck |
| `docker/postgres/.env.example` | Standalone env reference for the DB compose file |
| `docs/POSTGRES_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons postgres \
  --yes
```

Often combined with `fastapi-docker`:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-docker postgres \
  --yes
```

## Verify after scaffold

```sh
docker compose -f docker/postgres/compose.yml up -d
uv sync
uv run python -c "import psycopg"
```

See `template/docs/POSTGRES_GUIDE.md` for full usage, configuration, and troubleshooting.
