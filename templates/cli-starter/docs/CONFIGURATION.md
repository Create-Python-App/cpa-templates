# Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLI_LOG_LEVEL` | `INFO` | Example setting via `cli_app.config.load_settings()` |

Scaffold-time option (`cpa.config.json`):

| Option | Default | Description |
|--------|---------|-------------|
| `commandName` | `my-cli` | Console script name written to `[project.scripts]` |

## Compatible extensions

- `github-setup`, `development-container`
- Stack Docker overlays (`fastapi-docker`, etc.) are not a fit for a pure CLI;
  add a dedicated packaging story under DEPLOYMENT.md if you need containers.
