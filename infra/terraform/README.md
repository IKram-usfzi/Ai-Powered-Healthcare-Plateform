# AWS Terraform (Phase 8 — stretch, not currently applied)

**Status: written, not deployed.** The platform's actual deployment target is
local Docker Compose (`infra/docker-compose.yml`), per `deccission.md`
ADR-004 — Docker Compose is the mandatory exam-brief deliverable and AWS is
an optional stretch. This module exists so an AWS deployment can be stood up
later without design work at that point; nothing here has been `terraform
apply`'d, and no AWS resources are currently running from it.

Implements the topology documented in `architecture.md` §5 and `TRD.md` §8.

## What this provisions

| Resource | Purpose |
|---|---|
| VPC + 1 public / 2 private subnets | Public subnet for the app EC2 instance; private subnets (2 AZs, RDS's DB subnet group requirement) keep RDS off the internet |
| Internet Gateway + public route table | Outbound/inbound internet for the public subnet only |
| Security groups | App SG: 22/80/443 only (22 restricted to `ssh_allowed_cidr`). DB SG: 5432 from the app SG only — never a public CIDR |
| `aws_instance.app` (EC2, t3.micro) | Runs the whole stack via Docker Compose, bootstrapped by `user_data.sh.tpl` (installs Docker, clones the repo, starts `docker compose -f docker-compose.yml -f docker-compose.aws.yml up -d`) |
| `aws_eip.app` | Stable public IP across instance stop/start |
| `aws_db_instance.postgres` (RDS, db.t3.micro) | Single-AZ PostgreSQL 16, private subnet, encrypted, not publicly accessible |
| `aws_budgets_budget.monthly_cap` | Billing alarm at 80% actual / 100% forecasted of `budget_limit_usd` — `TRD.md` §8 requires this exist *before* any deployment activity |

Not provisioned (out of scope for this pass, noted in `architecture.md` §5 as
optional): CloudFront, Route53/a real domain, ElastiCache (Redis stays a
local container on the EC2 instance, same as the local profile).

## Before running this for real

1. **Confirm your AWS Free Tier model.** `TRD.md` §8: accounts created after
   15 Jul 2025 get a ~$100–200 credit (6-month window) instead of 12 months
   of always-free EC2/RDS hours. Check which applies to your account before
   assuming any of this is free.
2. Create an EC2 key pair in the target region and note its name
   (`ssh_key_name`): `aws ec2 create-key-pair --key-name globalcare --query
   'KeyMaterial' --output text > globalcare.pem && chmod 400 globalcare.pem`
3. Find your own public IP for `ssh_allowed_cidr` (e.g. `curl -s
   ifconfig.me`) — never leave SSH open to `0.0.0.0/0`.
4. `cp terraform.tfvars.example terraform.tfvars` and fill in real values.
   **Never commit `terraform.tfvars`** — it holds the DB password and your
   email (already gitignored).

## Usage

```bash
cd infra/terraform
terraform init
terraform plan    # review before applying — check instance/RDS sizing, budget amount
terraform apply
```

After `apply` finishes, `cloud-init` still needs a few minutes to install
Docker and bring the containers up. Check progress with:

```bash
ssh -i globalcare.pem ubuntu@$(terraform output -raw app_public_ip) \
  "tail -f /var/log/cloud-init-output.log"
```

Once it's up, the API is reachable at `http://<app_public_ip>:8000` and the
frontend at `http://<app_public_ip>:5173`. Two manual "day 2" steps this
module deliberately doesn't automate (they depend on a registered domain,
which is outside this module's scope):

- Point the frontend's `VITE_API_BASE_URL` (`infra/docker-compose.yml`,
  overridden per-environment) at the app's real public address instead of
  `localhost`, then `docker compose up -d --build frontend` on the instance.
- Put a TLS-terminating reverse proxy or CloudFront in front of port 80/443
  if this needs to be reachable over HTTPS (`Security.md` §4 requires TLS
  for all API traffic in the AWS profile) — plain HTTP on 80 is what the
  security group allows today, TLS termination is not yet wired up.

## Tearing down

```bash
terraform destroy
```

Destroys everything this module created, including the RDS instance
(`skip_final_snapshot = true` — no snapshot is kept). Nothing here has
`deletion_protection` enabled, by design, since this is meant to be
cheap to spin up and down for a demo, not a standing production database.
