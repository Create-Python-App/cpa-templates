# Testing Guide

## Unit tests (local, no AWS)

```sh
uv sync
uv run pytest
```

`tests/` covers `glue_etl/transforms.py` only. Those helpers take and return
plain dicts, so the suite needs neither Spark nor network access. Keep it that
way: new row-level logic belongs in `glue_etl/` with a test, not inside the
Glue script.

## Lint and types

```sh
uv run ruff check .
uv run mypy glue_etl
```

## What is not tested locally

- `jobs/etl_job.py` imports `pyspark` and `awsglue`, which exist only on the
  Glue runtime. It is type-ignored (`# type: ignore[import]`) and validated by
  review plus `terraform plan`, not by pytest.
- `terraform/` changes are checked with `terraform fmt -check` and
  `terraform plan` against a development AWS account.

## Scaffold check (bank CI parity)

```sh
REPO=/absolute/path/to/cpa-templates
CI=true uvx create-awesome-python-app my-app \
  --template "file://$REPO?subdir=templates/glue-etl-job" \
  --no-interactive
cd my-app && uv sync && uv run pytest
```
