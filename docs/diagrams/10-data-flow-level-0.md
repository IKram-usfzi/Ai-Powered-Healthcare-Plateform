# 10. Data Flow Diagram (Level 0 — Context)

**Source:** `docs/api-spec.md` (role tables), `docs/backend-schema.md`.

The whole platform as a single process, with the four external entities and the data crossing the boundary in each direction.

```mermaid
flowchart LR
    PAT(["Patient"])
    DOC(["Doctor"])
    ADM(["Administrator"])
    EXE(["Executive"])

    SYS["GlobalCare Platform<br/>(FastAPI + PostgreSQL + Redis + AI)"]

    PAT -->|"registration info, vitals readings,<br/>appointment requests"| SYS
    SYS -->|"appointment confirmations,<br/>consultation history, own records"| PAT

    DOC -->|"consultation summaries,<br/>status updates, AI assessment requests,<br/>alert acknowledgements"| SYS
    SYS -->|"assigned patients' records,<br/>schedules, alerts, AI predictions"| DOC

    ADM -->|"patient/provider/facility<br/>registration data"| SYS
    SYS -->|"registration & appointment<br/>operational reports"| ADM

    EXE -->|"dashboard requests"| SYS
    SYS -->|"KPIs, trends, provider activity,<br/>executive report exports"| EXE
```
