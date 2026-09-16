# Glue ETL Job

Batch ETL on AWS Glue with PySpark, job bookmarks, and the Data Catalog —
scaffolded with [create-awesome-python-app](https://github.com/Create-Python-App/create-python-app).
Deploys with [Terraform](https://developer.hashicorp.com/terraform) and keeps
row-level logic in pure, locally testable Python.

## Quick start

```sh
cp .env.example .env
uv sync
uv run pytest
```

Deploy (needs AWS credentials and Terraform):

```sh
cd terraform
terraform init
terraform apply
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run pytest` | Unit tests (no Spark, Glue, or AWS needed) |
| `uv run ruff check .` | Lint |
| `uv run mypy glue_etl` | Types |
| `terraform -chdir=terraform plan` | Preview infrastructure changes |

## Project layout

```text
glue_etl/      # importable package: settings + pure-Python transforms
jobs/          # Glue entrypoint script (runs on Glue, uploaded by Terraform)
terraform/     # IAM role, Catalog database, S3 script artifact, Glue job
tests/         # pytest suite for the transform helpers
docs/          # structure, config, testing, deployment
```

## Configuration

Copy `.env.example` to `.env`. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

Scaffold-time options:

| Option | Default | Description |
|--------|---------|-------------|
| `jobName` | `glue-etl-job` | Glue job name |
| `catalogDatabase` | `analytics` | Data Catalog database |
| `s3BucketPrefix` | `s3://my-data-lake` | S3 prefix for data and artifacts |
| `glueVersion` | `4.0` | Glue runtime version |
| `workerType` | `G.1X` | Glue worker type |
| `dpuNumber` | `2` | Number of workers |

## Docs

- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [AGENTS.md](AGENTS.md) · [CONTRIBUTING.md](CONTRIBUTING.md)
