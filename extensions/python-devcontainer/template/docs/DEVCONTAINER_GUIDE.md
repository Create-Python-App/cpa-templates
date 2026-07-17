# Dev Container Guide

## Overview

The **python-devcontainer** extension opens the project in a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) with Python 3.12 and [uv](https://docs.astral.sh/uv/). It is editor-focused and does not replace **python-docker** for deployment or CI image builds. You can use both: Dev Container for daily coding, Docker Compose for integration testing.

## What it adds

| Path | Purpose |
|------|---------|
| `.devcontainer/devcontainer.json` | VS Code Dev Container config |
| `.devcontainer/Dockerfile` | Python 3.12 base image + uv installer |

### Pre-configured editor features

- **Extensions:** Python, Ruff, debugpy
- **Settings:** Format on save with Ruff
- **Ports:** `8000` forwarded with label "FastAPI"
- **Post-create:** `uv sync` runs automatically after container build

## Usage

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) running on the host
- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (or Cursor / compatible fork)

### Open the container

1. **Command Palette** → **Dev Containers: Reopen in Container**
2. Wait for the image build and `uv sync` (`postCreateCommand`)
3. Start the API from the integrated terminal:

```sh
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Port `8000` is forwarded — open http://localhost:8000/docs.

### With python-postgres

The Dev Container does not start Postgres automatically. Options:

1. Run Postgres on the host: `docker compose -f docker/postgres/compose.yml up -d` (from a host terminal).
2. Use Docker-in-Docker or a `dockerComposeFile` override in a custom `devcontainer.json` (not included by default).

Set `DATABASE_URL` in `.env` to reach Postgres on `host.docker.internal` (or the host LAN IP) when the DB runs outside the dev container.

## Configuration

| Knob | Where | Notes |
|------|-------|-------|
| Python version | `.devcontainer/Dockerfile` base tag | Keep aligned with `requires-python` |
| Editor extensions | `devcontainer.json` → `customizations.vscode.extensions` | Add/remove as needed |
| Post-create | `postCreateCommand` | Default `uv sync` |
| Forwarded ports | `forwardPorts` / `portsAttributes` | Default `8000` |
| Compose integration | `dockerComposeFile` + `service` | Optional multi-service stack |

## Verification

1. **Reopen in Container** completes without build errors.
2. Terminal: `uv --version` and `python --version` (3.12) work.
3. `uv sync` succeeds (also runs as `postCreateCommand`).
4. `uv run ruff check .` and `uv run pytest` pass.
5. `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` — `curl -s http://localhost:8000/api/v1/healthz` returns health OK.
6. VS Code / Cursor shows Python and Ruff extensions active in the container.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Build fails on uv install | Network / curl blocked | Retry; check corporate proxy settings |
| `uv: command not found` | PATH missing uv install dir | Ensure Dockerfile sets `PATH` to include uv |
| Port not reachable on host | Forwarding disabled | Confirm `forwardPorts` includes `8000` |
| Cannot reach host Postgres | Wrong hostname from container | Use `host.docker.internal` (Docker Desktop) or host gateway IP |
| Extensions missing | Cache / offline install | Rebuild container without cache |

## Resources

- [Dev Containers spec](https://containers.dev/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [uv](https://docs.astral.sh/uv/)
