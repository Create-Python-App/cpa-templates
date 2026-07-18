# Quality checklist (django-api) — M1

## Required

- [x] Feature apps under `apps/` with serializers / services / views / urls
- [x] Docs suite: PROJECT_STRUCTURE, API, CONFIGURATION, TESTING_GUIDE, DEPLOYMENT, TYPING
- [x] README, AGENTS, CONTRIBUTING present
- [x] OpenAPI via drf-spectacular (`/schema/`, `/docs/`)
- [x] pytest-django health test
- [x] Ruff + mypy/pyright configured
- [x] Feature scaffold lives under `docs/examples/` (not an installed app)
- [x] Compatible with `django-docker` and `postgres` extensions
