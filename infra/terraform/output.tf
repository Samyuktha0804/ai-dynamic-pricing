output "s3_bucket_name" {
  value = aws_s3_bucket.datalake.id
}

output "ecr_repo_url" {
  value = aws_ecr_repository.pricing_api.repository_url
}
