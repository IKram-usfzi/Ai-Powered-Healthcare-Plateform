# Deployment Guide

**Related:** `installation-guide.md`, `architecture.md` §5, `TRD.md` §8, `deccission.md` ADR-004/ADR-027

GlobalCare has two deployment profiles. Only the first is required by the exam brief; the second is an optional stretch that exists as infrastructure-as-code but has never been applied to a real AWS account.

## Profile 1 — Local Docker Compose (mandatory, the actual current deployment)

This is the platform's real, running deployment for this capstone. Full steps: `installation-guide.md`.

Summary: `docker compose -f infra/docker-compose.yml up -d --build`, run migrations, seed demo data. All 7 services (postgres, redis, opa, backend, frontend, prometheus, grafana) run as containers on one machine — no cloud account, no cost, works on an 8–16 GB laptop with no GPU (`TRD.md` §8).

To stop: `docker compose -f infra/docker-compose.yml down` (add `-v` to also drop the `postgres_data` volume and start from a clean database next time).

## Profile 2 — AWS (stretch, written but not deployed — ADR-027)

`infra/terraform/` implements the topology in `architecture.md` §5: a VPC with a public subnet (EC2 running the same Docker Compose stack) and private subnets (RDS PostgreSQL), security groups restricting inbound traffic to 22/80/443, and an AWS Budgets billing alarm. It is `terraform validate`-clean but has never been `terraform apply`'d — no AWS resources exist from this project.

If you want to actually deploy it:

1. Read `infra/terraform/README.md` in full first — it covers the AWS Free Tier caveat (account age matters), creating an SSH key pair, and finding your own IP for the security group.
2. `cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars` and fill in real values. Never commit this file.
3. ```bash
   cd infra/terraform
   terraform init
   terraform plan   # review before applying
   terraform apply
   ```
4. Wait a few minutes for `cloud-init` to install Docker and start the stack on the new EC2 instance (`ssh ubuntu@$(terraform output -raw app_public_ip) "tail -f /var/log/cloud-init-output.log"`).
5. Two manual steps this module deliberately doesn't automate (both depend on a registered domain, which is out of scope): point `VITE_API_BASE_URL` at the instance's real public address, and put a TLS-terminating reverse proxy or CloudFront in front of it if HTTPS is required (`Security.md` §4).
6. `terraform destroy` when done — no snapshot is kept (`skip_final_snapshot = true`), so this is meant to be cheap to spin up and down for a demo, not a standing deployment.

Full detail, including the exact resources provisioned and what's deliberately out of scope (CloudFront, Route53, ElastiCache): `infra/terraform/README.md`.

## Choosing a profile

Use Profile 1 unless you specifically need to demonstrate a live internet-reachable deployment (e.g. for the viva's AWS-related scenario questions) — in which case Profile 2 exists and is ready, but costs real money and needs an AWS account with billing set up (`TRD.md` §8's Free Tier notes).
