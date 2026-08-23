# 3. Detailed System Architecture Diagram

**Source:** `docs/architecture.md` §3 (Component Breakdown) and §4 (Module → Architecture Mapping), refined against the real implementation.

```mermaid
flowchart LR
    subgraph M1["Module 1 — Patient & Provider Management"]
        direction TB
        m1a["/auth/*, /patients, /providers,<br/>/facilities, /reports/registration"]
    end
    subgraph M2["Module 2 — Telemedicine"]
        direction TB
        m2a["/appointments, /consultations,<br/>/providers/{id}/schedule,<br/>/reports/appointments"]
    end
    subgraph M3["Module 3 — Remote Patient Monitoring"]
        direction TB
        m3a["/monitoring/readings,<br/>/monitoring/alerts"]
    end
    subgraph M4["Module 4 — AI Health Risk Assessment"]
        direction TB
        m4a["/ai/risk-assessment,<br/>/ai/predictions/{patientId},<br/>/ai/model/metadata"]
    end
    subgraph M5["Module 5 — Executive Dashboard"]
        direction TB
        m5a["/dashboard/overview, /dashboard/trends,<br/>/dashboard/provider-activity,<br/>/reports/executive"]
    end

    PG[("PostgreSQL")]
    REDIS[("Redis")]
    AI["AI/ML Service"]

    M1 --> PG
    M2 --> PG
    M2 -.->|"schedule cache"| REDIS
    M3 --> PG
    M3 -->|"de-dup check"| REDIS
    M4 --> PG
    M4 --> AI
    AI --> PG
    M5 --> PG
    M5 -.->|"cache hot aggregates"| REDIS
```

| Component | Responsibility |
|---|---|
| React frontend | All user-facing screens across the four personas; consumes REST APIs |
| FastAPI backend | Business logic, validation, auth issuance/verification, orchestration across DB/cache/AI service |
| PostgreSQL | Durable system of record for all clinical/operational entities |
| Redis | Ephemeral/fast-path data: KPI caching, alert de-duplication, session & rate-limit state |
| AI/ML service | Preprocessing, model training/inference for health risk classification |
| Prometheus + Grafana | Metrics collection and visualization |
| OPA | Policy-based authorization decisions (role-gated endpoints — `deccission.md` ADR-024) |
| Trivy | Vulnerability scanning of images/dependencies |
