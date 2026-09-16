# AGENTS.md – AI Interaction & Execution Guide (Humans: see CONTRIBUTING.md & docs/)

## Authoritative references

| Topic | Source |
|-------|--------|
| Architecture | docs/PROJECT_STRUCTURE.md |
| Configuration | docs/CONFIGURATION.md |
| Testing | docs/TESTING_GUIDE.md |
| Deployment | docs/DEPLOYMENT.md |
| Typing | docs/TYPING.md |

## Key commands

| Command | Purpose |
|---------|---------|
| `uv run pytest` | Unit tests (no AWS) |
| `uv run ruff check .` | Lint |
| `uv run mypy glue_etl` | Types |
| `terraform -chdir=terraform plan` | Preview infra changes |

## Task work protocol

1. Add row-level logic to `glue_etl/transforms.py` as pure functions over dicts.
2. Keep Spark I/O in `jobs/etl_job.py`; it only runs on the Glue runtime.
3. Pass runtime values as Glue job arguments; read them with `getResolvedOptions`.
4. Cover new helpers with pytest; do not require Spark, Glue, or AWS in unit tests.
5. Update docs when introducing job arguments, tables, or partitions.

## Guardrails

- Do not import `pyspark` or `awsglue` outside `jobs/` — the package must import cleanly anywhere.
- Do not hardcode bucket names, databases, or account IDs in code — use settings / job arguments.
- Do not commit `.env`, `*.tfstate`, or AWS credentials.
- Flag large dependency additions for human confirmation.
