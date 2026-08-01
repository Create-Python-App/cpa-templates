# API

## Base URL and versioning

- Development: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`
- Default API prefix (scaffold option `apiPrefix`): `/api/v1`

Tip: send a custom `X-Request-ID` while testing locally so you can correlate
HTTP responses with application logs.

## Health endpoint

- `GET {apiPrefix}/healthz`
  - Returns the standard `APIResponse` envelope
  - `dev_code`: `HEALTH_OK`
  - `data`: `{ "status": "ok" }`

Example (`apiPrefix=/api/v1`):

```http
GET /api/v1/healthz
```

```json
{
  "success": true,
  "status_code": 200,
  "dev_code": "HEALTH_OK",
  "message": "Service is healthy",
  "data": { "status": "ok" },
  "errors": [],
  "metadata": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-07-16T12:00:00Z"
  }
}
```

## Standard response envelope

Feature routes should return `APIResponse[T]` from
`app.schemas.common.responses`. Success and error payloads share the same shape:

```json
{
  "success": true,
  "status_code": 200,
  "dev_code": "RESOURCE_ACTION",
  "message": "Human-readable summary",
  "data": {},
  "errors": [],
  "metadata": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-07-16T12:00:00Z"
  }
}
```

Validation error example (`422`):

```json
{
  "success": false,
  "status_code": 422,
  "dev_code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "data": null,
  "errors": [
    { "field": "name", "message": "String should have at least 1 character" }
  ],
  "metadata": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-07-16T12:00:00Z"
  }
}
```

## `dev_code` conventions

| Situation | Suggested `dev_code` |
|-----------|----------------------|
| Health OK | `HEALTH_OK` |
| List success | `<RESOURCE>_LISTED` |
| Retrieve success | `<RESOURCE>_RETRIEVED` |
| Create success | `<RESOURCE>_CREATED` |
| Update success | `<RESOURCE>_UPDATED` |
| Delete success | `<RESOURCE>_DELETED` |
| Not found | `NOT_FOUND` |
| Conflict | `CONFLICT` |
| Validation | `VALIDATION_ERROR` |
| Unexpected failure | `INTERNAL_ERROR` |

## Request IDs

`RequestIDMiddleware` (`app/core/middleware.py`):

1. Reads `X-Request-ID` when present, otherwise generates a UUID.
2. Stores it on `request.state.request_id`.
3. Echoes it as the `x-request-id` response header.
4. Includes it in `metadata.request_id` for enveloped responses.

## Adding endpoints

1. Create or extend a feature under `app/features/<name>/`.
2. Expose routes from `router.py` and keep business logic in `service.py`.
3. Mount the feature router from `app/api/router.py`.
4. Prefer `make_item_response` / `make_error_response` helpers so clients always
   see the same envelope.

See [`PROJECT_STRUCTURE.md`](./PROJECT_STRUCTURE.md) for the feature copy
scaffold under `app/features/_feature_template_/`.
