# Redis

Adds a Redis client dependency, env docs, and a local Compose service.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `redis` |
| `app/core/redis_client.py` | `get_redis()` helper |
| `docker/redis/compose.yml` | Redis 7 Alpine + healthcheck |
| `.env.example.append` | `REDIS_URL` |

## Quick start

```sh
docker compose -f docker/redis/compose.yml up -d
uv sync
uv run python -c "from app.core.redis_client import get_redis; print(get_redis().ping())"
```
