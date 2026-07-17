# Project Structure

`fastapi-starter` uses a feature-based architecture inspired by
Create-Node-App's `react-vite-starter` and the NaNLABS FastAPI boilerplate.

## Layout

```text
app/
  main.py                         # FastAPI app setup and router mounting
  api/
    router.py                     # Compose feature routers
  core/
    config.py                     # Environment-backed settings
    exception_handlers.py         # Global API error envelopes
    logging_config.py             # Logging setup
    middleware.py                 # Request ID middleware
  features/
    health/
      router.py                   # HTTP endpoints for the health feature
      service.py                  # Feature business logic
      schemas.py                  # Feature request/response schemas
    _feature_template_/
      README.md                   # Copy-paste guide for new features
      router.py
      service.py
      schemas.py
  schemas/
    common/
      responses.py                # APIResponse envelope helpers
tests/
  test_health.py
```

## Adding A Feature

1. Copy `app/features/_feature_template_` to `app/features/<feature_name>`.
2. Rename imports from `app.features._feature_template_` to your feature module.
3. Define Pydantic models in `schemas.py`.
4. Keep business rules and external calls in `service.py`.
5. Expose HTTP endpoints from `router.py`.
6. Mount the feature router in `app/api/router.py`.

## Response Envelope

Feature routes should return `APIResponse[T]` from
`app.schemas.common.responses`. This keeps success, error, metadata, and request
ID handling consistent across the API.

## Request IDs

`RequestIDMiddleware` reads `X-Request-ID` when provided or creates a UUID. The
ID is available at `request.state.request_id`, returned in response metadata,
and echoed in the `x-request-id` response header.

## Typing

Annotate routers, services, and schemas. Prefer concrete return types such as
`APIResponse[HealthStatus]` over untyped dicts. See [TYPING.md](./TYPING.md).

## Related docs

- [API.md](./API.md) — envelope and endpoints
- [CONFIGURATION.md](./CONFIGURATION.md) — env and tooling
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) — pytest patterns
