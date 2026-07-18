# Dev Container (extension bank)

Maintainer-facing notes for the **development-container** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `.devcontainer/devcontainer.json` | VS Code / Cursor Dev Container config |
| `.devcontainer/Dockerfile` | Python 3.12 base + uv installer |
| `docs/DEVCONTAINER_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons development-container \
  --yes
```

## Verify after scaffold

In VS Code / Cursor: **Dev Containers: Reopen in Container**, then:

```sh
uv --version
uv run pytest
```

See `template/docs/DEVCONTAINER_GUIDE.md` for full usage, configuration, and troubleshooting.
