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
