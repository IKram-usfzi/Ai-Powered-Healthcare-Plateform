# 8. Enterprise Network Architecture Diagram

**Source:** `docs/architecture.md` §5, `docs/TRD.md` §8 — now grounded in the real Terraform resources authored (not yet applied — `deccission.md` ADR-027) in `infra/terraform/`.

```mermaid
flowchart TB
    INTERNET(["Internet"])

    subgraph VPC["VPC — 10.20.0.0/16"]
        IGW["Internet Gateway"]

        subgraph PUB["Public subnet — 10.20.1.0/24"]
            EC2["EC2 t3.micro<br/>aws_instance.app<br/>Docker Compose:<br/>backend, frontend, redis, opa<br/>(Prometheus/Grafana: opt-in)"]
        end

        subgraph PRIV["Private subnets — 10.20.11.0/24, 10.20.12.0/24"]
            RDS[("RDS PostgreSQL 16<br/>db.t3.micro, single-AZ<br/>encrypted, not publicly accessible")]
        end
    end

    INTERNET --> IGW
    IGW --> PUB
    EC2 -->|"5432, app SG → db SG only"| RDS

    SGAPP["App SG: 22 (ssh_allowed_cidr only) / 80 / 443"] -.-> EC2
    SGDB["DB SG: 5432 from App SG only"] -.-> RDS

    BUDGET["aws_budgets_budget<br/>80% actual / 100% forecasted<br/>of budget_limit_usd"] -.->|"billing alarm"| VPC
```

Not yet provisioned (noted as optional in `architecture.md` §5): CloudFront/Route53 in front of the app, and a TLS-terminating reverse proxy — `infra/terraform/README.md` documents both as manual "day 2" steps this module deliberately doesn't automate.
