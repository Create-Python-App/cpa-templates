# Redis (extension bank)

Maintainer-facing notes for the **python-redis** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `redis` into project dependencies |
| `app/core/redis_client.py` | `get_redis()` helper |
| `docker/redis/compose.yml` | Redis 7 Alpine + healthcheck |
| `.env.example.append` | `REDIS_URL` |
| `docs/REDIS_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-redis \
  --yes
```

Often combined with `python-docker`:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-docker python-redis \
  --yes
```

## Verify after scaffold

```sh
docker compose -f docker/redis/compose.yml up -d
uv sync
uv run python -c "from app.core.redis_client import get_redis; print(get_redis().ping())"
```

See `template/docs/REDIS_GUIDE.md` for full usage, configuration, and troubleshooting.
