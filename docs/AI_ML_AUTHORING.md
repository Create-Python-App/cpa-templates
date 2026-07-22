# AI/ML authoring guide

How to add AI/ML templates and extensions to `cpa-templates` without creating a
combinatorial catalog. Parent epic: [#71](https://github.com/Create-Python-App/cpa-templates/issues/71).

## Decision tree: template vs extension

| Question | Template | Extension |
|----------|----------|-----------|
| New project topology / framework? | Yes (e.g. sklearn MLOps layout) | No |
| Optional capability on FastAPI? | No | Yes (`fastapi-*`) |
| GitHub Actions / CT/CD? | Never in base template | Yes (`all-mlops-github-actions`) |
| Data modality (tabular/sequence/image)? | No | Prefer modality packs |
| Distributed training? | No | Framework-specific extension |

**Do not** add a new chat template type. Chat/RAG/agents are FastAPI extensions on
`fastapi-starter` (`type: fastapi-backend`).

**Do not** clone a monolithic SaaS-AI starter (CNA M3 flagship pattern). Compose
extensions instead.

## Categories

| Slug | Use for |
|------|---------|
| `ai-ml-applications` | FastAPI AI capability extensions |
| `mlops` | MLOps framework starters and MLOps-specific extensions |
| Reuse `ci`, `observability`, `database`, `containers`, `security` | Cross-cutting packs |

## Template types

| Type | Canonical template dir |
|------|------------------------|
| `mlops-sklearn` | `mlops-sklearn-starter` |
| `mlops-pytorch` | `mlops-pytorch-starter` (future) |
| `mlops-tensorflow` | `mlops-tensorflow-starter` (future) |

Keep using `fastapi-backend` for AI app extensions — do not invent `chat-*` types.

Update when adding types:

- `scripts/ci/registry.py::CANONICAL_TEMPLATE_BY_TYPE`
- `scripts/ci/validate-registry.py::STACK_PREFIX_BY_TYPE` (e.g. `mlops-sklearn` → `mlops-sklearn` or use `all-*`)

## Quality and CI rules

1. Default tests are **CPU-only**, fast, and use synthetic/fixture data.
2. No mandatory GPU/CUDA dependencies.
3. No network calls or real API keys in tests — placeholders in `.env.example` only.
4. GitHub Actions for MLOps live in extensions, not base templates.
5. **Bare L1** jobs for every AI/ML template even with zero extensions (#92).
6. **L2 runs pytest** in the generated project (#92).
7. L3 profiles stay small — never stack every AI extension (CNA #309 anti-pattern).

## `incompatibleWith` matrix (#91)

Declare conflicts in `templates.json` before merging conflicting pairs.

| Extension A | Extension B | Reason / resolution |
|-------------|-------------|---------------------|
| `fastapi-ai-chat` | `fastapi-langgraph-chat` | Both may own `/chat` — either set `incompatibleWith` or document non-overlapping routes before shipping LangGraph |
| Competing `all-mlops-*-data` packs that overwrite the same data paths | each other | Prefer one modality pack per profile |

`fastapi-ai-chat` and `fastapi-ai-guardrails` are **compatible** (guardrails are hooks).

## Extension constraints

- Use `template/` so bank `README.md` does not overwrite the project README.
- Ship `template/docs/<TOPIC>_GUIDE.md` and `template/docs/README.md.append`.
- Partial `pyproject.toml` overlays for dependencies.
- Ship tests for generated paths the extension adds (or document mount steps + unit tests).
- Do **not** embed `.github/workflows` in FastAPI AI extensions — compose `github-setup` or `all-mlops-github-actions`.

## Related docs

- [MLOPS_CONTRACT.md](./MLOPS_CONTRACT.md)
- [AUTHORING.md](./AUTHORING.md)
- [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md)
- [TESTING.md](./TESTING.md)
