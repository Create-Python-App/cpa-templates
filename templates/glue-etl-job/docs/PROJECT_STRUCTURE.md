# Project Structure

```text
glue-etl-job/
├── cpa.config.json          # scaffold options (job name, database, S3 prefix, …)
├── pyproject.toml           # uv manifest (boto3 runtime; pytest/ruff/mypy dev)
├── .env.example             # local overrides (copy to .env, never commit it)
├── glue_etl/
│   ├── __init__.py
│   ├── config.py            # pydantic-settings (rendered from scaffold options)
│   └── transforms.py        # pure-Python row helpers (no Spark imports)
├── jobs/
│   └── etl_job.py           # Glue entrypoint: bookmarks, Spark I/O, Catalog writes
├── terraform/
│   ├── main.tf              # IAM role, Catalog database, script object, Glue job
│   ├── variables.tf         # aws_region input
│   └── outputs.tf           # job name, database, script location, role ARN
├── tests/
│   └── test_transforms.py   # pytest suite (stdlib + package only)
└── docs/                    # this guide set
```

## Why this split

- `glue_etl/` must import cleanly anywhere (developer laptop, CI). It never
  imports `pyspark` or `awsglue`.
- `jobs/etl_job.py` only executes on the Glue runtime, where Spark and the
  Glue libraries are provided. Terraform uploads it to S3 and points the job
  at it.
- `terraform/` owns everything the script references by name: the IAM role,
  the Catalog database, the S3 script key, and the job arguments. Renaming on
  one side without the other breaks deploys, which is why Terraform ships in
  the base template instead of as an optional extension.

## Adding a new source

1. Add a pure function to `glue_etl/transforms.py` plus a test in
   `tests/test_transforms.py`.
2. Call it from `jobs/etl_job.py` after the read step.
3. If the new source needs a new job argument, add it to the `getResolvedOptions`
   list, to `default_arguments` in `terraform/main.tf`, and to
   `docs/CONFIGURATION.md`.
