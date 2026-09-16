# Configuration

Settings live in `glue_etl/config.py` (pydantic-settings) and load from the
environment / `.env`. The Glue script itself receives runtime values as job
arguments (see `terraform/main.tf` `default_arguments`).

| Variable | Default (scaffold) | Purpose |
|----------|--------------------|---------|
| `JOB_NAME` | `glue-etl-job` | Glue job name (also drives bookmarks) |
| `CATALOG_DATABASE` | `analytics` | Data Catalog database |
| `S3_BUCKET_PREFIX` | `s3://my-data-lake` | S3 prefix for `raw/`, `processed/`, `scripts/`, `tmp/` |
| `GLUE_VERSION` | `4.0` | Documented runtime version (infra uses it) |
| `WORKER_TYPE` | `G.1X` | Documented worker type (infra uses it) |
| `DPU_NUMBER` | `2` | Documented worker count (infra uses it) |
| `AWS_REGION` | `us-east-1` | Region for local tooling and Terraform default |

Scaffold-time options in `cpa.config.json`:

| Option | Default | Description |
|--------|---------|-------------|
| `jobName` | `glue-etl-job` | Written into job script, Terraform, and config |
| `catalogDatabase` | `analytics` | Catalog database name |
| `s3BucketPrefix` | `s3://my-data-lake` | Must be a bare bucket URL; layouts append `raw/`, `processed/`, `scripts/`, `tmp/` |
| `glueVersion` | `4.0` | `glue_version` on the Terraform job |
| `workerType` | `G.1X` | `worker_type` on the Terraform job |
| `dpuNumber` | `2` | `number_of_workers` on the Terraform job |

## Job bookmarks

Bookmarks are enabled in Terraform (`--job-bookmark-option = job-bookmark-enable`)
and driven by `--JOB_NAME` in `jobs/etl_job.py` (`job.init(...)` / `job.commit()`).
Each run therefore only processes newly arrived objects under `<prefix>/raw/`.

## Compatible extensions

None yet — this template is intentionally template-only for v1. Future
packaging variants (for example CDK or CloudFormation) can ship as extensions
once the base exists.
