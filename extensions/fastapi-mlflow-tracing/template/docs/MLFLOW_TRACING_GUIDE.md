# MLflow Tracing Guide

## Overview

The **fastapi-mlflow-tracing** extension adds generic [MLflow](https://mlflow.org/) tracing infrastructure to your FastAPI project. Tracing is **disabled by default** — set `MLFLOW_ENABLED=true` to opt in. When disabled, the extension is a true no-op: MLflow is not imported and no connections are attempted.

This extension provides foundational primitives. It does **not** include AI, LangChain, or model-specific wrappers.

## How it works

MLflow is configured automatically at scaffold time — no edits to `app/main.py` are needed. The extension registers `configure_mlflow_tracing` in `app/core/providers.py` via the CPA auto-wiring mechanism.

`configure_mlflow_tracing()` sets the **tracking URI** at app startup. Experiment selection (`mlflow.set_experiment()`) is deferred to call sites — calling it at startup would eagerly create the experiment in the tracking store (a network call in MLflow 3.x), which is inappropriate for an app startup hook. Set the experiment before starting each run:

```python
import mlflow

def record_inference(prompt: str) -> str:
    mlflow.set_experiment("my-feature")  # select or create experiment here
    with mlflow.start_run():
        result = call_model(prompt)
        mlflow.log_metric("latency_ms", ...)
        return result
```

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `mlflow>=3.15.0` |
| `app/core/mlflow_tracing.py` | `MLflowTracingSettings`, `configure_mlflow_tracing()`, `maybe_start_span`, `set_attribute` |
| `app/core/providers.py.append.template` | Auto-registers `configure_mlflow_tracing` in the app provider registry |
| `.env.example.append` | Documents `MLFLOW_*` variables |
| `tests/test_mlflow_tracing.py` | Offline unit tests |

## Local development — run the MLflow UI

```sh
# 1. Start a local tracking server (stores runs under mlruns/)
uv run mlflow server --host 127.0.0.1 --port 5000

# 2. Set env vars (or add to .env)
export MLFLOW_ENABLED=true
export MLFLOW_TRACKING_URI=http://localhost:5000

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

Use `maybe_start_span` and `set_attribute` in any feature:

```python
from app.core.mlflow_tracing import maybe_start_span

def generate_chat_response(messages: list[dict]) -> str:
    with maybe_start_span("llm_inference", **{"llm.provider": "openai"}) as span:
        response = call_openai_api(messages)
        return response
```

**Privacy Boundary:** Do not record raw prompts, completions, or payload data by default. Only log them behind an explicit opt-in configuration flag.

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `MLFLOW_ENABLED` | `false` | Set to `true` to enable |
| `MLFLOW_TRACKING_URI` | `http://localhost:5000` | Remote server or `file:///path` |
| `MLFLOW_EXPERIMENT_NAME` | `fastapi-app` | Used as a suggested experiment name for your runs |

## Security considerations

- **Never** include authentication headers, API keys, request bodies, or passwords in span attributes.
- Set `MLFLOW_TRACKING_URI` to a `file://` path in CI and development to avoid sending data to a remote server.
- Do not commit `.env` to source control.

## Production configuration

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
