# FastAPI AI Extension Route Ownership Conventions

This document defines route ownership conventions for FastAPI AI extensions in `cpa-templates`. Following these conventions prevents route collisions when multiple AI extensions are combined.

Parent issue: [#120](https://github.com/Create-Python-App/cpa-templates/issues/120) · Parent track: [#73](https://github.com/Create-Python-App/cpa-templates/issues/73)

---

## Base Routes (owned by `fastapi-starter`)

| Route | Feature | Owner |
|-------|---------|-------|
| `/api/v1/healthz` | Health check | `fastapi-starter` (health feature) |
| `/api/v1/health/ready` | Readiness check | `fastapi-starter` (health feature) |

**Do not** override these routes in extensions.

---

## AI Extension Route Ownership

| Extension | Base Path | Full Routes | Notes |
|-----------|-----------|-------------|-------|
| `fastapi-ai-chat` | `/api/v1/chat` | `POST /api/v1/chat` | Single chat endpoint; mounted via `.append` |
| `fastapi-rag-pgvector` | `/api/v1/rag` | `POST /api/v1/rag/query`, `POST /api/v1/rag/ingest` | Not yet mounted — see *Future Extensions* |
| `fastapi-langgraph-chat` (planned) | `/api/v1/chat` | — | **Conflicts with `fastapi-ai-chat`** — see [#91](https://github.com/Create-Python-App/cpa-templates/issues/91) |

---

## Convention: Use Dedicated Sub-paths per Extension

Each AI extension **must** own a unique sub-path under `/api/v1/`:

| Extension Category | Reserved Prefix |
|--------------------|-----------------|
| Chat / conversational | `/api/v1/chat` |
| RAG / retrieval | `/api/v1/rag` |
| Agents / workflows | `/api/v1/agents` |
| Embeddings / vector ops | `/api/v1/embeddings` |
| Guardrails / safety | `/api/v1/guardrails` |

When adding a new extension, claim a prefix before implementation. Reserve it in this table by opening a PR updating this document.

---

## Convention: Prefix All Extension Routes

Every extension router **must** be mounted under its claimed prefix. Do not mount at `/api/v1/` directly.

```python
# ✅ Good: extension owns /api/v1/chat
from app.features.chat.router import router as chat_router
router.include_router(chat_router, prefix="/chat")

# ❌ Bad: mounts at root, collides with health + other extensions
router.include_router(chat_router)
```

In `cpa-templates`, this is enforced by the `.append` mechanism — extensions add to `app/api/router.py` which already has `/api/v1` prefix.

---

## Convention: Declare `incompatibleWith` for Overlapping Paths

If two extensions **must** share a prefix (e.g., competing chat implementations), declare mutual `incompatibleWith` in `templates.json`:

```json
{
  "name": "FastAPI AI Chat",
  "slug": "fastapi-ai-chat",
  "incompatibleWith": ["fastapi-langgraph-chat"],
  "...": "..."
}
```

See [#91](https://github.com/Create-Python-App/cpa-templates/issues/91) and [AI_ML_AUTHORING.md](../AI_ML_AUTHORING.md#incompatiblewith-matrix-91) for the full matrix.

---

## Middleware Hooks

Extensions that add middleware **must** document the hook name and purpose:

| Extension | Middleware | Purpose |
|-----------|------------|---------|
| `fastapi-auth-jwt` | `AuthMiddleware` | JWT validation on protected routes |

Future AI extensions adding middleware should add entries here.

---

## Adding a New AI Extension (Checklist)

1. [ ] Claim a unique prefix in the *AI Extension Route Ownership* table above
2. [ ] Mount routers with that prefix (use `.append` mechanism)
3. [ ] If conflicting with an existing extension on the same prefix, add `incompatibleWith` to both entries in `templates.json`
4. [ ] Add entry to this table
5. [ ] Document any middleware hooks in the *Middleware Hooks* table
6. [ ] Update `docs/recipes/FASTAPI_AI_ROUTE_OWNERSHIP.md` in the same PR

---

## Validation

L0 registry validation (via `scripts/ci/validate-registry.py`) checks:

- No two enabled extensions declare overlapping route prefixes
- `incompatibleWith` pairs are symmetric

See `scripts/ci/validate-registry.py` for implementation.
