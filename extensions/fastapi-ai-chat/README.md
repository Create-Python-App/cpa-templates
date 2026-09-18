# FastAPI AI Chat (extension bank)

Maintainer-facing notes for the **fastapi-ai-chat** extension in `cpa-templates`.

## Compatible types

| Template type | Compatible? | Notes |
|---------------|-------------|-------|
| `fastapi-backend` | ✅ Yes | Requires `app/features/` layout and `app/api/router.py.append` |
| `django-backend` | ❌ No | Not compatible — Django uses `config/urls.py.append` and a different app layout |
| `celery-worker` | ❌ No | Not compatible — no HTTP routing surface |
| `cli-app` | ❌ No | Not compatible — CLI apps have no web framework |
| `uv-workspace` | ❌ No | Not compatible — workspace templates don't include FastAPI by default |

## Copied into generated projects (via `template/`)

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `langchain-core` |
| `app/features/chat/` | Schemas, langchain-core provider abstraction (mock only), `/chat` router |
| `app/api/router.py.append` | Auto-mounts the chat router in `app/api/router.py` |
| `tests/test_chat.py` | Offline tests against an isolated router-only test app |
| `.env.example.append` | Provider/model/API key placeholders |
| `docs/AI_CHAT_GUIDE.md` | Long-form guide for the generated project |

The bank `README.md` (this file) stays **outside** `template/` so it does not
overwrite the project README.

The chat router is mounted automatically via the `.append` mechanism — no changes to `app/api/router.py` are needed.

## Environment variables

| Variable | Default | Notes |
|----------|---------|-------|
| `AI_CHAT_PROVIDER` | `mock` | Only `mock` is implemented in this MVP; any other value returns a 500 |
| `AI_CHAT_MODEL` | `mock-chat` | Echoed back in the response; has no effect on the mock |
| `AI_CHAT_API_KEY` | *(blank)* | Placeholder for a future real provider — never commit a real key |
| `AI_CHAT_MAX_INPUT_CHARS` | `4000` | Total character budget across all messages in a request |

See `template/docs/AI_CHAT_GUIDE.md` for full configuration and troubleshooting details.

## `incompatibleWith`

This extension does **not** currently declare any `incompatibleWith` entries. It is compatible with all standard FastAPI starter addons that don't ship a conflicting `app/api/router.py` or `app/features/chat/` path.

If you are authoring a competing AI chat provider extension (e.g. `fastapi-ai-chat-langchain`), declare mutual incompatibility here to prevent path collisions on `router.py.append`.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-ai-chat \
  --no-interactive
```

## Verify after scaffold

```sh
uv sync
uv run pytest tests/test_chat.py
```

See `template/docs/AI_CHAT_GUIDE.md` for full usage, configuration, and troubleshooting.
