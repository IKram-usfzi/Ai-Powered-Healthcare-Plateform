output "app_public_ip" {
  description = "Public IP of the EC2 app instance (stable across stop/start via the Elastic IP)."
  value       = aws_eip.app.public_ip
}

output "app_ssh_command" {
  description = "SSH into the app instance to check on the Docker Compose bootstrap (cloud-init logs: /var/log/cloud-init-output.log)."
  value       = "ssh ubuntu@${aws_eip.app.public_ip}"
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint (host:port). Not internet-reachable — only the app security group can connect."
  value       = aws_db_instance.postgres.endpoint
}

output "rds_address" {
  description = "RDS PostgreSQL host only (no port) — matches what user_data.sh.tpl writes into .env as RDS_ENDPOINT."
  value       = aws_db_instance.postgres.address
}

output "vpc_id" {
  description = "VPC ID, for reference when adding future resources (e.g. CloudFront, Route53)."
  value       = aws_vpc.main.id
}
