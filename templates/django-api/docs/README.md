# Django API docs

- Prefer DRF `APIView` / viewsets under `api/` as the project grows.
- Keep health probes unauthenticated.
- When adding Postgres, update `DATABASES` in `config/settings.py` and prefer env-driven DSN parsing.
