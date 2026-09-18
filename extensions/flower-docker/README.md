# Flower for Celery (extension bank)

Maintainer-facing notes for the **flower-docker** extension.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `Dockerfile` | uv-based image; Celery worker CMD (flower runs via `celery flower`) |
| `.dockerignore` | Excludes `.venv`, caches, git metadata |
| `compose.yml` | Dev compose: `redis` + `worker` + `flower` (port 5555) with healthchecks |
| `compose.prod.yml` | Prod overlay (`restart: always`, concurrency, healthchecks) |
| `pyproject.toml` | Adds `flower>=2.0.1` dependency |
| `.env.example.append` | `FLOWER_BASIC_AUTH` / `FLOWER_PORT` examples |
| `docs/FLOWER_GUIDE.md` | Long-form guide |
| `docs/README.md.append` | Index bullet |

Compose includes a Redis broker. Env vars are `BROKER_URL` / `RESULT_BACKEND`
(matching `worker/config.py`). Flower listens on `5555` and shares the same
image + broker env. Healthcheck probes `http://localhost:5555` via Python.

`flower-docker` is **incompatible** with `celery-docker` — both ship
`Dockerfile` / `compose.yml` for `celery-worker` and would overwrite the same
paths (see `templates.json:c/incompatibleWith`). Use one or the other.

## Apply

```sh
uvx create-awesome-python-app my-worker \
  --template celery-worker \
  --addons flower-docker \
  --yes
```

To try Flower alongside an existing `celery-docker` scaffold, replace the
addon:

```sh
uvx create-awesome-python-app my-worker \
  --template celery-worker \
  --addons flower-docker \
  --yes
```

## Verify

```sh
docker compose up --build
# Flower dashboard: http://localhost:5555
# Worker log shows ready; flower log shows "Visit me at http://0.0.0.0:5555"
```

With basic auth (optional):

```sh
# .env
FLOWER_BASIC_AUTH=user:password
docker compose up --build
# http://user:password@localhost:5555
```
