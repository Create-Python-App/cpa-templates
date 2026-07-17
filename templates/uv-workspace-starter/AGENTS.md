# AGENTS.md — AI Interaction & Execution Guide

This file is for AI assistants. Humans: see `README.md` and `docs/`.

## Authoritative references (do not duplicate content here)

| Topic | Source of truth |
|-------|-----------------|
| Monorepo layout | `docs/PROJECT_STRUCTURE.md` |
| Day-to-day workflow | `docs/DEVELOPMENT_WORKFLOW.md` |
| Publishing members | `docs/RELEASING.md` |

## Key commands (run from the workspace root)

| Command | Purpose |
|---------|---------|
| `uv sync` | Install every workspace member into one `.venv` |
| `uv run ruff check .` | Lint all members |
| `uv run pyright` | Type-check all members |
| `uv run pytest` | Test all members |
| `uv build --all-packages` | Build wheels/sdists for all members |

## Operating principles

- Reuse before build: prefer adding to an existing `packages/*` library over new deps.
- Keep libraries in `packages/`, deployables in `apps/`.
- Type safety across members (every package ships `py.typed`).
- Small, isolated changes; avoid cross-member churn without justification.

## Execution protocol (member work)

1. Identify the target member under `apps/` or `packages/` (justify new ones).
2. Audit existing shared libraries before adding utilities or dependencies.
3. Depend on a local library via its distribution name **plus**
   `[tool.uv.sources] "<name>" = { workspace = true }`.
4. After changes, run `uv run ruff check .`, `uv run pyright`, `uv run pytest`.

## Guardrails

- Do NOT invent package names or paths.
- Do NOT create circular dependencies between members.
- Flag additions of >1 new external dependency for confirmation.
- New members must live under `packages/*` or `apps/*` so the workspace globs pick them up.

## Package creation checklist

- `pyproject.toml` with `name`, `version`, `requires-python = ">=3.12"`.
- `[build-system]` using `hatchling` and `[tool.hatch.build.targets.wheel] packages = ["src/<module>"]`.
- `src/<module>/` layout with a `py.typed` marker.
- Tests under `tests/` (or an explicit deferral with a reason).

## Post-change report

Return a short bullet summary: files touched, new dependencies (if any),
lint/type/test status, and any deferred items.
