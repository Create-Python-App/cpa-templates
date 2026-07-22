# AI Chat guide

POST `/api/v1/chat` with `{"messages":[{"role":"user","content":"..."}]}`.

Default provider is `mock` (no network). Set `AI_CHAT_PROVIDER` / `AI_CHAT_MODEL` /
`AI_CHAT_API_KEY` in `.env` when wiring a real provider.

Compose with `fastapi-ai-guardrails` for input/output checks.
