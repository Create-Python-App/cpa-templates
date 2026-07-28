# MLflow Tracing Guide

## Overview

The **fastapi-mlflow-tracing** extension adds generic [MLflow](https://mlflow.org/) tracing infrastructure to your FastAPI project. Tracing is **disabled by default** — set `MLFLOW_ENABLED=true` to opt in. When disabled, the extension is a true no-op: MLflow is not imported and no connections are attempted.

This extension provides foundational primitives. It does **not** include AI, LangChain, or model-specific wrappers.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `mlflow>=2.15.0` |
| `app/core/mlflow_tracing.py` | `MLflowTracingSettings`, `configure_mlflow_tracing(app)`, `maybe_start_span`, `set_attribute` |
| `.env.example` entries | Documents `MLFLOW_*` variables |
| `tests/test_mlflow_tracing.py` | Offline unit tests |

## Wire it up

1. Import and call `configure_mlflow_tracing()` near the top of your `app/main.py`.

```python
from app.core.mlflow_tracing import configure_mlflow_tracing

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

Use `maybe_start_span` to instrument specific sections safely:

```python
from app.core.mlflow_tracing import maybe_start_span, set_attribute

with maybe_start_span("database-query", table="users") as span:
    results = fetch_data()
    set_attribute("result_count", len(results))
```

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `MLFLOW_ENABLED` | `false` | Set to `true` to enable |
| `MLFLOW_TRACKING_URI` | `http://localhost:5000` | Remote server or `file:///path` |
| `MLFLOW_EXPERIMENT_NAME` | `fastapi-app` | Groups related traces |

## Using this from an AI extension

**AI-specific spans are intentionally out of scope for this extension.**

This extension does not implement AI logic directly. Instead, it exposes `maybe_start_span` and `set_attribute` so future AI extensions (e.g., chat APIs) can cleanly record LLM spans. 

Per the repository's span schema ([Issue #112](https://github.com/Create-Python-App/cpa-templates/issues/112)), AI spans should use the `llm_inference` name and standard `llm.*` attributes.

```python
from app.core.mlflow_tracing import maybe_start_span

def generate_chat_response(messages: list[dict]) -> str:
    # Safely creates an MLflow span if MLFLOW_ENABLED=true
    with maybe_start_span(
        "llm_inference", 
        **{
            "llm.provider": "openai",
            "llm.model": "gpt-4",
            "llm.stream": False,
        }
    ) as span:
        response = call_llm(messages)
        
        # Only log raw prompts/completions if the user opts in via an LLM_TRACE_PAYLOAD flag
        # (This protects user privacy by default)
        
        return response
```

## Security considerations

- Only `http.method`, `http.path`, and `http.status_code` are recorded as span attributes by the middleware.
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
