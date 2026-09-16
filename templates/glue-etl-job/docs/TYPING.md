# Typing

`glue_etl/` and `tests/` are fully typed (`mypy`, strictness matching the bank:
`warn_return_any`, `warn_unused_configs`).

## Runtime-only imports

`jobs/etl_job.py` imports `pyspark` and `awsglue`, which are provided by the
Glue runtime and absent locally. Those imports carry `# type: ignore[import]`
and the script is excluded from `mypy` `files` (only `glue_etl` and `tests`
are checked). Never import `jobs/` from `glue_etl/` or `tests/`.

`boto3` / `botocore` have no bundled stubs, so `pyproject.toml` sets
`ignore_missing_imports` for them, mirroring how sibling templates handle
unstubbed drivers.

## Rules

- Public helpers in `glue_etl/transforms.py` need annotated signatures.
- Keep Spark `Row`/`DataFrame` handling inside `jobs/etl_job.py`, converting
  at the boundary (`row.asDict()` in, `spark.createDataFrame` out).
- Run `uv run mypy glue_etl` before opening a PR.
