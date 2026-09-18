# Deployment

## Prerequisites

- AWS credentials with Glue, S3, and IAM permissions
- [Terraform](https://developer.hashicorp.com/terraform) >= 1.6
- An S3 bucket matching `S3_BUCKET_PREFIX` (Terraform does not create the bucket)

## Deploy

```sh
cd terraform
terraform init
terraform plan
terraform apply
```

Apply uploads `jobs/etl_job.py` to `<prefix>/scripts/etl_job.py` and registers
the Glue job with bookmarks enabled.

## Run the job

```sh
aws glue start-job-run --job-name glue-etl-job
```

Drop CSV files with a header row under `<prefix>/raw/` first; cleaned output
lands partitioned by `ingestion_date` under `<prefix>/processed/`.

## Production checklist

- [ ] Bucket, database, and job names from reviewed Terraform state, not defaults
- [ ] `max_concurrent_runs = 1` still appropriate for the source arrival rate
- [ ] Bookmarks verified: a second run with no new objects writes nothing
- [ ] No account IDs or credentials in `.env`, job arguments, or docs
- [ ] CloudWatch log groups retention set for the job runs

## Observability

Glue streams driver/executor logs to CloudWatch automatically. Add metric
filters or alarms on `ERROR` in the `/aws-glue/jobs/` log group when moving
beyond manual runs.
