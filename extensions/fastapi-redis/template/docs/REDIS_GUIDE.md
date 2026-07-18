# Redis Guide

## Overview

The **fastapi-redis** extension adds a Redis client dependency, a small `get_redis()` helper, env docs, and a local Redis 7 Compose service under `docker/redis/`.

Use it for cache, sessions, rate limits, or as a broker when pairing with Celery later.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `redis>=5.2.0` into project dependencies |
| `app/core/redis_client.py` | `get_redis()` returning a decoded-response client |
| `docker/redis/compose.yml` | Redis 7 Alpine + volume + `redis-cli ping` healthcheck |
| `.env.example.append` | Appends `REDIS_URL` to root `.env.example` |

## Usage

### Redis only

```sh
docker compose -f docker/redis/compose.yml up -d
uv sync
uv run python -c "from app.core.redis_client import get_redis; print(get_redis().ping())"
```

### With fastapi-docker

```sh
docker compose -f compose.yml -f docker/redis/compose.yml up --build
```

Inside Compose, point `REDIS_URL` at the service hostname `redis` (for example `redis://redis:6379/0`). From the host machine, use `localhost`.

### In application code

```python
from app.core.redis_client import get_redis

r = get_redis()
r.set("greeting", "hello")
print(r.get("greeting"))
```

## Configuration

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `REDIS_URL` | `redis://localhost:6379/0` | Host URL for local Compose |

`get_redis()` uses `decode_responses=True` so values are `str` rather than `bytes`.

## Verification

1. `docker compose -f docker/redis/compose.yml up -d` — `redis` reaches healthy.
2. `docker compose -f docker/redis/compose.yml ps` shows `healthy` for `redis`.
3. `uv run python -c "from app.core.redis_client import get_redis; assert get_redis().ping()"` after `uv sync`.
4. Optional: `redis-cli -u redis://localhost:6379/0 ping` returns `PONG`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Connection refused` on localhost:6379 | Compose not running | Start `docker/redis/compose.yml` |
| App cannot reach Redis in Docker | Using `localhost` inside API container | Use hostname `redis` in `REDIS_URL` |
| Bytes instead of strings | Custom client without decode | Prefer `get_redis()` or pass `decode_responses=True` |
| `import redis` fails | Overlay not merged / sync skipped | Confirm `pyproject.toml` deps and re-run `uv sync` |

## Resources

- [redis-py documentation](https://redis-py.readthedocs.io/)
- [Redis Docker Hub](https://hub.docker.com/_/redis)
- [Compose multiple files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)
