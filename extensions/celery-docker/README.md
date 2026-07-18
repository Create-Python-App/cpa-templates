# Docker for Celery (extension bank)

Maintainer-facing notes for the **celery-docker** extension.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `Dockerfile` | uv-based image; Celery worker CMD |
| `.dockerignore` | Excludes `.venv`, caches, git metadata |
| `compose.yml` | Dev worker compose (bind mount) |
| `compose.prod.yml` | Prod worker overlay |
| `docs/DOCKER_GUIDE.md` | Long-form guide |
| `docs/README.md.append` | Index bullet |

Compose includes a Redis broker. Env vars are `BROKER_URL` / `RESULT_BACKEND`
(matching `worker/config.py`). Pair with `postgres` only when the worker also
needs a database.

## Apply

```sh
uvx create-awesome-python-app my-worker \
  --template celery-worker \
  --addons celery-docker \
  --yes
```

## Verify

```sh
docker compose up --build
```
