# AGENTS.md – AI Interaction & Execution Guide (Human contributors: see CONTRIBUTING.md & docs/)

This file is intentionally scoped only for AI assistants (Cursor, Copilot Chat, PR automation bots).
Humans: read CONTRIBUTING.md and the documents under docs/.

## 1. Authoritative References (Never Reproduce Content Here)

| Topic | Source of Truth |
|-------|-----------------|
| Project architecture | docs/PROJECT_STRUCTURE.md |
| API contracts & envelope | docs/API.md |
| Testing patterns | docs/TESTING_GUIDE.md |
| Deployment | docs/DEPLOYMENT.md |
| Configuration (env, Ruff, uv) | docs/CONFIGURATION.md |
| Typing (mypy / pyright) | docs/TYPING.md |

(If a file ends with `.template` it will be materialized during project generation—still treat it as authoritative.)

## Key Commands

Run from the project root after `uv sync`:

| Command | Purpose |
|---------|---------|
| `uv run uvicorn app.main:app --reload` | Dev ASGI server |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run mypy app` | Type check (mypy) |
| `uv run pyright` | Type check (pyright) |
| `uv run pytest` | Tests |

## 2. Operating Principles (AI Perspective)

- Documentation-first
- Reuse-before-build
- Type safety always (no unvetted `Any`)
- Deterministic, incremental changes
- Explicit assumption logging

## 3. AI Execution Protocol (FastAPI Feature Work)

When asked to add/modify API logic:

1. Locate or create the appropriate feature folder under `app/features/*` (justify new ones)
2. Read related docs referenced above before proposing code
3. Prefer extending existing router / service / schema patterns
4. Present proposed file tree + diff plan BEFORE writing code
5. After code changes: list validation steps (format, lint, type check, tests)

## 4. Guardrails (Must Enforce)

- Do NOT fabricate file paths, endpoint contracts, or library versions
- Do NOT bypass the `APIResponse` envelope for feature routes without rationale
- Do NOT put business logic solely in routers—use `service.py`
- ALWAYS flag large dependency additions (>1 lib) for human confirmation
- ALWAYS surface security-sensitive changes (CORS, secrets, auth) for review

## 5. Feature Creation Checklist

- Feature package under `app/features/<name>/` with router, service, schemas
- Router mounted in `app/api/router.py`
- Stable `dev_code` values documented or consistent with docs/API.md
- Test coverage for happy path + envelope fields
- Docs updated when introducing a new cross-cutting concept

## 6. When the AI Should Ask or Refuse

Ask if: feature scope unclear, conflicting patterns, missing target directory.
Refuse if: asked to bypass validation, remove type safety, or duplicate an existing documented feature.

## 7. Post-Change Assistant Report

Return a bullet summary:

- Files touched (concise)
- New dependencies (if any)
- Lint / type / test status
- Suggested manual QA steps
- Deferred items (tests, docs)

---
Maintained automatically by create-awesome-python-app FastAPI template provisioning.
Humans: stop reading—go to CONTRIBUTING.md + docs/.
