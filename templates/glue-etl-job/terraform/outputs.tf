output "job_name" {
  description = "Name of the Glue ETL job."
  value       = aws_glue_job.etl.name
}

output "catalog_database" {
  description = "Data Catalog database holding the output tables."
  value       = aws_glue_catalog_database.analytics.name
}

output "script_location" {
  description = "S3 location of the deployed job script."
  value       = "s3://${aws_s3_object.job_script.bucket}/${aws_s3_object.job_script.key}"
}

output "job_role_arn" {
  description = "IAM role assumed by the Glue job."
  value       = aws_iam_role.job_role.arn
}
