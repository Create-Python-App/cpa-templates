# OpenTelemetry tracing

This extension adds a small OpenTelemetry bootstrap for FastAPI so you can inspect request flows locally (console exporter) or ship spans to an OTLP collector.

## How it works

OpenTelemetry is configured automatically at scaffold time — no edits to `app/main.py` are needed. The extension registers `configure_telemetry` in `app/core/providers.py` via the CPA auto-wiring mechanism; `app/main.py` calls `setup_app(app)` which runs all registered providers at startup.

Initialization is a **no-op** when `OTEL_ENABLED` is unset or false, so local development stays quiet until you opt in.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges OpenTelemetry API/SDK + FastAPI/logging instrumentation + OTLP/HTTP exporter |
| `app/core/telemetry.py` | `configure_telemetry(app)` helper |
| `.env.example.append` | Documents `OTEL_*` variables |

## Configure

Add these values to your `.env` file:

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=my-api
# Optional — when empty, spans print to the console (great for local debug)
OTEL_EXPORTER_OTLP_ENDPOINT=
```

To send spans to a collector (for example the OTEL Collector or Jaeger OTLP):

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=my-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
```

## Verify

Start the app and hit an endpoint — you should see span output in the terminal when `OTEL_EXPORTER_OTLP_ENDPOINT` is empty:

```sh
uv sync
OTEL_ENABLED=true OTEL_SERVICE_NAME=my-api uv run uvicorn app.main:app
```

## Resources

- [OpenTelemetry Python](https://opentelemetry-python.readthedocs.io/)
- [FastAPI instrumentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html)
- [OTLP exporter](https://opentelemetry-python.readthedocs.io/en/latest/exporter/otlp/otlp.html)
