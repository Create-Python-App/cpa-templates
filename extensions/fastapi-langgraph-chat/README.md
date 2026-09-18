# FastAPI LangGraph Chat (extension bank)

Maintainer-facing notes for the **fastapi-langgraph-chat** extension in `cpa-templates`.

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
| `pyproject.toml` | Merges `langgraph` + `langchain-core` |
| `app/features/agent_chat/` | Schemas, tools, state graph, service, `/agent/chat` router |
| `app/api/router.py.append` | Auto-mounts the agent router in `app/api/router.py` |
| `tests/test_agent_chat.py` | Offline graph + endpoint tests |
| `.env.example.append` | Provider/model/char-budget placeholders |
| `docs/LANGGRAPH_CHAT_GUIDE.md` | Long-form guide for the generated project |

The bank `README.md` (this file) stays **outside** `template/` so it does not
overwrite the project README.

The agent router is mounted automatically via the `.append` mechanism — no changes to `app/api/router.py` are needed.

## Environment variables

| Variable | Default | Notes |
|----------|---------|-------|
| `AGENT_CHAT_PROVIDER` | `mock` | Only `mock` is implemented in this MVP; any other value returns a 500 |
| `AGENT_CHAT_MODEL` | `mock-agent` | Echoed back in the response; has no effect on the mock |
| `AGENT_CHAT_MAX_INPUT_CHARS` | `4000` | Total character budget across all messages in a request |

See `template/docs/LANGGRAPH_CHAT_GUIDE.md` for full configuration and troubleshooting details.

## `incompatibleWith`

This extension does **not** declare any `incompatibleWith` entries. Its route
(`/agent/chat`) does not collide with `fastapi-ai-chat` (`/chat`), and its
file paths (`app/features/agent_chat/`) are unique.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-langgraph-chat \
  --no-interactive
```

## Verify after scaffold

```sh
uv sync
uv run pytest tests/test_agent_chat.py
```

See `template/docs/LANGGRAPH_CHAT_GUIDE.md` for full usage, configuration, and troubleshooting.
