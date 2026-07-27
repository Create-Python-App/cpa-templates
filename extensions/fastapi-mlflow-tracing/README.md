# MLflow Tracing (extension bank)

Maintainer-facing notes for the **fastapi-mlflow-tracing** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `mlflow>=2.15.0` into project dependencies |
| `app/core/mlflow_tracing.py` | `MLflowTracingSettings`, `configure_mlflow_tracing()`, `maybe_start_span`, `set_attribute` |
| `.env.example.append` | `MLFLOW_ENABLED`, tracking URI, experiment name |
| `tests/test_mlflow_tracing.py` | Offline unit tests using a local `file://` tracking directory |
| `docs/MLFLOW_TRACING_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

Like `fastapi-sentry` and `fastapi-opentelemetry`, this extension exposes a generic `configure_mlflow_tracing(app)` helper and safe generic primitives for future AI extensions to use.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-mlflow-tracing \
  --yes
```

## Verify after scaffold

```sh
uv sync
# Confirm disabled by default (no-op, no MLflow import)
uv run python -c "from app.core.mlflow_tracing import configure_mlflow_tracing; configure_mlflow_tracing()"
# Run offline tests
uv run pytest tests/test_mlflow_tracing.py -v
```

See `template/docs/MLFLOW_TRACING_GUIDE.md` for full usage, configuration, and troubleshooting.
