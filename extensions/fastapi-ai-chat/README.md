# FastAPI AI Chat (extension bank)

Maintainer-facing notes for the **fastapi-ai-chat** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

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

## Compatible Types

| Template Type | Notes |
|---------------|-------|
| `fastapi-backend` | Requires `fastapi-starter` or compatible FastAPI base |

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

### Test Commands

| Command | Description |
|---------|-------------|
| `uv run pytest tests/test_chat.py` | Run chat-specific tests |
| `uv run pytest` | Run full test suite |

## Environment Variables

Set these in `.env` or export them before running the generated project:

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_CHAT_PROVIDER` | `mock` | Provider: `mock`, `openai`, `anthropic`, `google`, etc. |
| `AI_CHAT_MODEL` | `mock-chat` | Model identifier for the chosen provider |
| `AI_CHAT_API_KEY` | *(empty)* | API key for the provider |
| `AI_CHAT_MAX_INPUT_CHARS` | `4000` | Maximum input characters per request |

## `incompatibleWith` Notes

This extension may conflict with other chat implementations that mount routes at the same path:

- **`fastapi-langgraph-chat`** (planned): Both extensions own `/api/v1/chat`. Use `incompatibleWith` in `templates.json` when LangGraph variant lands. See [#91](https://github.com/Create-Python-App/cpa-templates/issues/91).

Declare mutual `incompatibleWith` on both extensions in `templates.json` before merging.

See `template/docs/AI_CHAT_GUIDE.md` for full usage, configuration, and troubleshooting.
