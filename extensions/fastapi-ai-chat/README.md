# FastAPI AI Chat (extension bank)

MVP chat extension for `fastapi-starter` ([#77](https://github.com/Create-Python-App/cpa-templates/issues/77)).

Copied via `template/`:

| Path | Purpose |
|------|---------|
| `app/features/chat/` | `/chat` endpoint, schemas, mock provider |
| `app/api/router.py` | Mounts health + chat (canonical L2 composition) |
| `tests/test_chat.py` | Offline tests with mock provider |
| `.env.example.append` | Provider/model/API key placeholders |
| `docs/AI_CHAT_GUIDE.md` | Generated-project guide |

No `.github/workflows` here — compose `github-setup`.
