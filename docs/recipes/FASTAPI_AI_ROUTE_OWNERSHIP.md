# Route ownership for FastAPI AI extensions

FastAPI AI extensions ([#73](https://github.com/Create-Python-App/cpa-templates/issues/73)) all overlay the same `app/` tree, so two of them can end up mounting the same path. This note records which prefixes are taken and how to claim a new one.

## How routes are mounted

`app/main.py` includes the API router at `settings.api_prefix`, which defaults to `/api/v1`. Feature routers declare their own prefix with `APIRouter(prefix="/chat", tags=["chat"])`, and an extension attaches its router by appending to `app/api/router.py` through `app/api/router.py.append`. The final path is the API prefix plus the feature prefix. Do not hardcode the API prefix in a feature module, since it is a scaffold option the user chooses.

## Prefixes in use

| Prefix | Owner | Feature module |
|---|---|---|
| `/chat` | `fastapi-ai-chat` | `app/features/chat/` |
| `/auth` | `fastapi-auth-jwt` | `app/features/auth/` |
| `/healthz` | `fastapi-starter` | `app/features/health/` |
| `/examples` | `fastapi-starter` | `app/features/_feature_template_/`, not mounted |
| `/rag` | unclaimed | see below |

`/ping`, `/`, `/docs` and `/redoc` belong to `app/main.py` and sit outside the API prefix.

A new extension should claim one prefix named after the capability rather than the vendor, keep that prefix on the `APIRouter` instead of in the path decorators, name the feature directory to match, and add a row to the table above in the same PR. If two extensions genuinely need the same prefix, declare symmetric `incompatibleWith` in `templates.json` for both entries. CI checks the symmetry in `scripts/ci/validate-registry.py`.

## Why `/rag` is unclaimed

`fastapi-rag-pgvector` ships `app/features/rag/` with no `router.py`. It exposes `chunk_text`, `ingest_document` and `retrieve_context` for other features to import, so it composes with `fastapi-ai-chat` rather than competing for a prefix. An extension that wants retrieval over HTTP should add the router and claim `/rag` at the same time.

Do not put RAG endpoints under `/chat`. FastAPI matches routes in registration order, so a second router on an occupied path does not fail at startup; the later route is simply never reached.

## Middleware and app setup

Extensions that configure the app rather than serve a route register a provider in `app/core/providers.py.append.template`:

```python
@register
def _opentelemetry(app: FastAPI) -> None:
    from app.core.telemetry import configure_telemetry
    configure_telemetry(app)
```

`fastapi-cors`, `fastapi-opentelemetry`, `fastapi-mlflow-tracing`, `fastapi-sentry` and `fastapi-rate-limit` use this hook today. Providers run in addon order and `add_middleware` is LIFO, so the last one registered wraps the others. Keep the provider function thin and import its implementation inside the body. Middleware does not belong in a feature router.

Environment variables use one namespace per extension, appended through `.env.example.append`. `AI_CHAT_*`, `RAG_*`, `MLFLOW_*`, `OTEL_*`, `SENTRY_*`, `RATE_LIMIT_*` and `REDIS_*` are taken.
