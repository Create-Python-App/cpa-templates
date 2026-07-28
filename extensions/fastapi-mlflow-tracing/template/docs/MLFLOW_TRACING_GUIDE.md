# MLflow Tracing Guide

## Overview

The **fastapi-mlflow-tracing** extension adds generic [MLflow](https://mlflow.org/) tracing infrastructure to your FastAPI project. Tracing is **disabled by default** — set `MLFLOW_ENABLED=true` to opt in. When disabled, the extension is a true no-op: MLflow is not imported and no connections are attempted.

This extension provides foundational primitives. It does **not** include AI, LangChain, or model-specific wrappers.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `mlflow>=2.15.0` |
| `app/core/mlflow_tracing.py` | `MLflowTracingSettings`, `configure_mlflow_tracing()`, `maybe_start_span`, `set_attribute` |
| `.env.example` entries | Documents `MLFLOW_*` variables |
| `tests/test_mlflow_tracing.py` | Offline unit tests |

## Wire it up

In `app/main.py`, call `configure_mlflow_tracing()` during startup to set the tracking URI and active experiment (no-op when `MLFLOW_ENABLED=false`):

```python
from app.core.mlflow_tracing import configure_mlflow_tracing

# Create app...
app = FastAPI()

# Configure MLflow tracking URI and experiment
configure_mlflow_tracing()
```

## Local development — run the MLflow UI

```sh
# 1. Start a local tracking server (stores runs under mlruns/)
uv run mlflow server --host 127.0.0.1 --port 5000

# 2. Set env vars (or add to .env)
export MLFLOW_ENABLED=true
export MLFLOW_TRACKING_URI=http://localhost:5000
export MLFLOW_EXPERIMENT_NAME=my-api-dev

# 3. Start your FastAPI app
uv run uvicorn app.main:app --reload
```

Open http://localhost:5000 to view traces.

Alternatively, use a local file-based backend (no server required):

```env
MLFLOW_ENABLED=true
MLFLOW_TRACKING_URI=file:///absolute/path/to/mlruns
```

## Tracing individual code blocks

Future AI extensions can consume `maybe_start_span` and `set_attribute` directly:

```python
from app.core.mlflow_tracing import maybe_start_span

def generate_chat_response(messages: list[dict]) -> str:
    with maybe_start_span("llm_inference", **{"llm.provider": "openai"}) as span:
        response = call_openai_api(messages)
        return response
```

**Privacy Boundary:** By default, do not record raw prompts, completions, or raw payload data. AI-specific span schemas should adhere to standard structures (like those discussed in [Issue #112](https://github.com/Create-Python-App/cpa-templates/issues/112)). Only log payload tracing if hidden behind an explicit opt-in configuration flag.

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `MLFLOW_ENABLED` | `false` | Set to `true` to enable |
| `MLFLOW_TRACKING_URI` | `http://localhost:5000` | Remote server or `file:///path` |
| `MLFLOW_EXPERIMENT_NAME` | `fastapi-app` | Groups related traces |

## Using this from an AI extension

**AI-specific spans are intentionally out of scope for this extension.**

This extension is designed to be consumed by other extensions. If you are building an AI extension, you can use the provided primitives safely without worrying if tracing is actually enabled. `configure_mlflow_tracing()` is called during startup, setting up the active experiment and tracking server.

*Note: HTTP request spans are intentionally not captured by this extension. OpenTelemetry (`fastapi-opentelemetry`) owns the HTTP request layer.*

## Security considerations

- **Never** include authentication headers, API keys, request bodies, or passwords in span attributes.
- Set `MLFLOW_TRACKING_URI` to a `file://` path in CI and development to avoid sending data to a remote server.
- Do not commit `.env` to source control.

## Production configuration

For production, point at a secured MLflow Tracking Server:

```env
MLFLOW_ENABLED=true
MLFLOW_TRACKING_URI=https://mlflow.internal.example.com
MLFLOW_EXPERIMENT_NAME=my-api-prod
```

## Verification

```sh
# 1. Run offline tests
uv run pytest tests/test_mlflow_tracing.py -v

# 2. Smoke-test enabled path with local file backend
MLFLOW_ENABLED=true MLFLOW_TRACKING_URI=file:///tmp/mlruns \
  uv run python -c "from app.core.mlflow_tracing import configure_mlflow_tracing; configure_mlflow_tracing(); print('ok')"
```
