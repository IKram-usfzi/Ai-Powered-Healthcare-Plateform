#!/usr/bin/env bash
# Bootstraps the EC2 app instance: installs Docker, clones the app repo, and
# starts the AWS profile (RDS instead of local Postgres; Prometheus/Grafana
# trimmed per TRD.md §8's ~1GB-RAM note — see ../docker-compose.aws.yml).
# Rendered from this template by infra/terraform/ec2.tf's templatefile() call.
set -euo pipefail

apt-get update -y
apt-get install -y ca-certificates curl gnupg git

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

usermod -aG docker ubuntu

git clone ${app_repo_url} /opt/globalcare
cd /opt/globalcare/infra

# Values below are supplied by Terraform (aws_db_instance.postgres's real
# endpoint/credentials) — never hand-edit this file on the instance; re-run
# `terraform apply` and let it re-render user_data instead.
cat > .env <<ENV_EOF
POSTGRES_USER=${db_username}
POSTGRES_PASSWORD=${db_password}
POSTGRES_DB=${db_name}
RDS_ENDPOINT=${rds_endpoint}
ENV_EOF
chmod 600 .env

docker compose -f docker-compose.yml -f docker-compose.aws.yml up -d
