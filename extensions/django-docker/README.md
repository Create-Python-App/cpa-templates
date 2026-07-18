# Docker for Django (extension bank)

Maintainer-facing notes for the **django-docker** extension.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `Dockerfile` | uv-based image; `gunicorn config.wsgi` |
| `.dockerignore` | Excludes `.venv`, caches, git metadata |
| `compose.yml` | Dev compose (`runserver` + bind mount) |
| `compose.prod.yml` | Prod overlay (`gunicorn`, restart always) |
| `docs/DOCKER_GUIDE.md` | Long-form guide |
| `docs/README.md.append` | Index bullet |

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template django-api \
  --addons django-docker \
  --yes
```

## Verify

```sh
docker compose up --build
curl -s http://localhost:8000/api/healthz/
```
