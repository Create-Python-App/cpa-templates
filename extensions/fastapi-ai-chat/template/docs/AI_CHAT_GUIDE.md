# AI Chat Guide

## Overview

The **fastapi-ai-chat** extension adds a minimal `/chat` endpoint backed by LangChain's provider abstraction (`langchain-core`'s `BaseChatModel`), with a mock provider by default so it works offline with no API key. This establishes the pattern future FastAPI AI extensions build on — it intentionally does not include RAG, MCP, MLflow tracing, or a frontend.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `langchain-core` |
| `app/features/chat/schemas.py` | `ChatMessage`, `ChatRequest`, `ChatResponse` |
| `app/features/chat/providers.py` | `get_provider(name)` → `BaseChatModel`; `mock` uses `GenericFakeChatModel` |
| `app/features/chat/service.py` | Input-length validation, provider resolution, LangChain message mapping |
| `app/features/chat/router.py` | `POST /chat` |
| `.env.example.append` | `AI_CHAT_PROVIDER`, `AI_CHAT_MODEL`, `AI_CHAT_API_KEY`, `AI_CHAT_MAX_INPUT_CHARS` |

## How it works

The chat router is mounted automatically at scaffold time via the CPA auto-wiring mechanism — no edits to `app/api/router.py` are needed.

## Call the endpoint

```sh
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H 'content-type: application/json' \
  -d '{"messages":[{"role":"user","content":"hello"}]}'
```

Default provider is `mock` — no network call, no API key needed.

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `AI_CHAT_PROVIDER` | `mock` | Only `mock` is implemented in this MVP; any other value returns a 500 |
| `AI_CHAT_MODEL` | `mock-chat` | Echoed back in the response; has no effect on the mock |
| `AI_CHAT_API_KEY` | *(blank)* | Placeholder for a future real provider — never commit a real key |
| `AI_CHAT_MAX_INPUT_CHARS` | `4000` | Total character budget across all messages in a request |

## Verification

1. `uv run pytest tests/test_chat.py` — tests pass offline (schema validation, provider factory, roundtrip, oversized input, unknown provider).
2. `POST /api/v1/chat` with a `user` message returns a 200 with an `assistant` message.
3. Setting `AI_CHAT_MAX_INPUT_CHARS=5` and sending a longer message returns 400.
4. Setting `AI_CHAT_PROVIDER` to anything other than `mock` returns 500 (no real provider is implemented yet).

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `404` on `/chat` | Scaffold didn't apply the router append | Re-scaffold or verify `app/api/router.py` includes the chat router |
| `500 unknown AI_CHAT_PROVIDER` | Typo or unimplemented provider | Use `mock`, or wire a real provider via `langchain`'s `init_chat_model()` |
| `400` on valid-looking input | `AI_CHAT_MAX_INPUT_CHARS` too low | Raise the limit in `.env` |

## Resources

- [LangChain chat models](https://docs.langchain.com/oss/python/langchain/models)
- [langchain-core testing utilities](https://docs.langchain.com/oss/python/langchain/test)
- [FastAPI request body](https://fastapi.tiangolo.com/tutorial/body/)
