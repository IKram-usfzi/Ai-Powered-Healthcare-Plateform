# 9. Network Flow Diagram

**Source:** `infra/docker-compose.yml` (mandatory local profile — real, running), `infra/terraform/` (stretch AWS profile — written, not deployed).

## Local Docker Compose profile (the actual, current deployment)

```mermaid
flowchart LR
    HOST(["Host machine<br/>(student laptop)"])

    HOST -->|"localhost:5173"| FE["frontend container<br/>:5173"]
    HOST -->|"localhost:8000"| BE["backend container<br/>:8000"]
    HOST -->|"localhost:9090"| PROM["prometheus container<br/>:9090"]
    HOST -->|"localhost:3001"| GRAF["grafana container<br/>:3000"]
    HOST -->|"localhost:8181"| OPA["opa container<br/>:8181"]
    HOST -->|"localhost:5432"| PG["postgres container<br/>:5432"]
    HOST -->|"localhost:6379"| REDIS["redis container<br/>:6379"]

    FE -->|"REST, VITE_API_BASE_URL"| BE
    BE -->|"5432"| PG
    BE -->|"6379"| REDIS
    BE -->|"8181, allow_role decisions"| OPA
    BE -->|"exposes /metrics"| PROM
    PROM -->|"datasource"| GRAF

    subgraph NET["Docker bridge network (infra_default)"]
        FE
        BE
        PROM
        GRAF
        OPA
        PG
        REDIS
    end
```

## AWS profile (written, not deployed — `deccission.md` ADR-027)

```mermaid
flowchart LR
    CLIENT(["Client browser"]) -->|"80/443"| EC2["EC2 (public subnet)"]
    ADMIN(["Operator"]) -->|"22, ssh_allowed_cidr only"| EC2
    EC2 -->|"5432, app SG → db SG"| RDS[("RDS, private subnet")]

    EC2 -.->|"not internet-reachable"| RDS
    CLIENT -.->|"blocked — SG has no route"| RDS
```
