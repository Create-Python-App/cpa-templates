# Docker (extension bank)

Maintainer-facing notes for the **python-docker** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `Dockerfile` | uv-based Python 3.12 image |
| `.dockerignore` | Excludes `.venv`, caches, git metadata |
| `compose.yml` | Dev compose (bind mount + reload) |
| `compose.prod.yml` | Prod overlay (no reload, restart always) |
| `docs/DOCKER_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-docker \
  --yes
```

## Verify after scaffold

```sh
docker compose up --build
curl -s http://localhost:8000/api/v1/healthz
```

See `template/docs/DOCKER_GUIDE.md` for full usage, configuration, and troubleshooting.
