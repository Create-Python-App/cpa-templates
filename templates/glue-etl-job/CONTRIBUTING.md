# Contributing

## Setup

```bash
uv sync
uv run pytest
```

Terraform formatting (when changing `terraform/`):

```bash
terraform -chdir=terraform fmt -check
```

## Style

- Row-level logic in `glue_etl/` as pure, typed functions
- Ruff for lint/format
- Typed public function signatures

## Docs

Update the matching file under `docs/` when behaviour changes. Keep `AGENTS.md`
as a pointer table, not a second docs tree.

## Extensions

Template-only for now: Terraform ships in the base because the job script,
Catalog names, IAM role, and S3 keys reference each other and cannot deploy
separately.
