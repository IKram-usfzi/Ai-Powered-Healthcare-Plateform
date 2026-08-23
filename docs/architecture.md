# System Architecture

**Related:** `TRD.md`, `backend-schema.md`, `api-spec.md`, `flow.md`, `deccission.md`

## 1. Architectural Principles

- **Layered separation:** presentation (React) / API & business logic (FastAPI) / data (PostgreSQL, Redis) / AI service (Scikit-learn).
- **Stateless API layer:** session/auth state via JWT, not server memory, so the API tier can scale horizontally if ever needed.
- **Containers-first:** every service runs as a Docker container; Docker Compose is the source of truth for how services fit together.
- **Security and observability are cross-cutting**, not bolted on — JWT/OPA/Trivy and Prometheus/Grafana touch every layer.
- **Conceptual standards alignment** (FHIR, ISO, NIST, HIPAA/GDPR) is expressed in schema design and documentation, not by running the reference healthcare systems themselves.

## 2. High-Level Architecture (local / exam-mandatory profile)

```
                                   USERS
                 Patient        Doctor        Administrator      Executive
                    │              │                │                │
                    └──────────────┴────────┬───────┴────────────────┘
                                             ▼
                                  ┌─────────────────────┐
                                  │   React Frontend      │
                                  │ (UI per supplied        │
                                  │  template)               │
                                  └──────────┬───────────┘
                                             │ REST (JWT)
                                             ▼
                                  ┌─────────────────────┐
                                  │   FastAPI Backend      │
                                  │  Auth (JWT/RBAC)         │
                                  │  Patient/Provider API    │
                                  │  Telemedicine API         │
                                  │  Monitoring API            │
                                  │  AI Risk API                │
                                  │  Executive/Reporting API     │
                                  └───┬─────────┬─────┬───┘
                                      │         │     │
                     ┌────────────────┘         │     └───────────────┐
                     ▼                          ▼                     ▼
          ┌─────────────────┐       ┌────────────────────┐   ┌──────────────────┐
          │   PostgreSQL      │       │       Redis           │   │  AI/ML Service     │
          │  patients          │       │  dashboard cache       │   │  Scikit-learn       │
          │  providers         │       │  alert de-dup           │   │  Pandas / NumPy     │
          │  facilities        │       │  session/rate limit     │   │  trained on Synthea  │
          │  appointments      │       └────────────────────┘   └──────────────────┘
          │  consultations     │
          │  health_readings   │
          │  alerts            │
          │  predictions       │
          └─────────────────┘

     Cross-cutting: JWT + OPA (RBAC) + Trivy (image/dep scanning)
                    FastAPI metrics → Prometheus → Grafana
     Packaging:     Docker + Docker Compose (mandatory) | K3s/Kind (optional)
```

## 3. Component Breakdown

| Component | Responsibility |
|---|---|
| React frontend | All user-facing screens across the four personas; consumes REST APIs |
| FastAPI backend | Business logic, validation, auth issuance/verification, orchestration across DB/cache/AI service |
| PostgreSQL | Durable system of record for all clinical/operational entities |
| Redis | Ephemeral/fast-path data: KPI caching, alert de-duplication, session & rate-limit state |
| AI/ML service (in-process or sidecar) | Preprocessing, model training/inference for health risk classification |
| Prometheus + Grafana | Metrics collection and visualization |
| OPA | Policy-based authorization decisions |
| Trivy | Vulnerability scanning of images/dependencies |

## 4. Module → Architecture Mapping

| Module | Primary path |
|---|---|
| 1. Patient/Provider Registration | React → FastAPI → PostgreSQL |
| 2. Telemedicine Appointments | React → FastAPI → PostgreSQL (+ Redis schedule cache) |
| 3. Remote Patient Monitoring | Ingestion endpoint → FastAPI → PostgreSQL (readings/alerts) → Redis (de-dup) |
| 4. AI Health Risk Assessment | FastAPI → AI service → PostgreSQL (prediction history) |
| 5. Executive Dashboard | PostgreSQL/Redis aggregates → FastAPI reporting endpoints → React + Plotly |

## 5. Deployment Architecture — AWS Free-Tier (stretch profile)

```
                    Internet
                       │
                 ┌─────────────┐
                 │ CloudFront /  │  (Always-Free tier — hosts React build + MkDocs site)
                 │ Route53 (opt) │
                 └──────┬──────┘
                        │
                 ┌──────────────────────── VPC ────────────────────────┐
                 │  Public subnet                                        │
                 │   EC2 (t2.micro/t3.micro): Docker Compose               │
                 │     - FastAPI + React (or Nginx)                        │
                 │     - Redis                                               │
                 │     - Prometheus + Grafana (trimmed/demo-only)             │
                 │   Security Group: 22 / 80 / 443 only                       │
                 │                                                          │
                 │  Private subnet                                          │
                 │   RDS PostgreSQL (db.t3.micro / db.t4g.micro, single-AZ)   │
                 └───────────────────────────────────────────────────────┘
```

## 6. Mandatory Diagram Inventory (17 required — brief §8)

All 17 are real Mermaid diagrams-as-code under [`diagrams/`](diagrams/README.md) (Phase 9), each matching the actual implementation, not just this document's design-time sketches — see the linked index for the full list.

1. [Enterprise Digital Healthcare Architecture Diagram](diagrams/01-enterprise-architecture.md)
2. [High-Level Solution Architecture Diagram](diagrams/02-high-level-solution-architecture.md) (§2 above, refined)
3. [Detailed System Architecture Diagram](diagrams/03-detailed-system-architecture.md) (§3/§4 above, refined)
4. [Telemedicine Platform Architecture Diagram](diagrams/04-telemedicine-architecture.md)
5. [Remote Patient Monitoring Architecture Diagram](diagrams/05-remote-monitoring-architecture.md)
6. [AI Health Risk Assessment Architecture Diagram](diagrams/06-ai-risk-assessment-architecture.md)
7. [Clinical Workflow Architecture Diagram](diagrams/07-clinical-workflow-architecture.md)
8. [Enterprise Network Architecture Diagram](diagrams/08-enterprise-network-architecture.md) (§5 above — AWS VPC topology, grounded in the real `infra/terraform/`)
9. [Network Flow Diagram](diagrams/09-network-flow.md)
10. [Data Flow Diagram (Level 0)](diagrams/10-data-flow-level-0.md)
11. [Data Flow Diagram (Level 1)](diagrams/11-data-flow-level-1.md)
12. [Telemedicine Workflow Diagram](diagrams/12-telemedicine-workflow.md)
13. [Remote Monitoring Workflow Diagram](diagrams/13-remote-monitoring-workflow.md)
14. [AI Prediction Workflow Diagram](diagrams/14-ai-prediction-workflow.md)
15. [Healthcare Operations Workflow Diagram](diagrams/15-healthcare-operations-workflow.md)
16. [Database Entity Relationship Diagram](diagrams/16-database-erd.md) (attribute-level; design-level version in `backend-schema.md` §1)
17. [Sequence Diagram](diagrams/17-end-to-end-sequence.md) — registration → appointment scheduling → remote monitoring → AI assessment → executive reporting

Diagrams 4, 5, 6, 7, 12–15, 17 draw their content from `flow.md`; diagram 16 from `backend-schema.md`. All are Mermaid (diagrams-as-code), diffable in Git and rendered natively on GitHub; Draw.io remained unused — nothing needed presentation-specific layout beyond what Mermaid handles.

## 7. Architectural Decisions

See `deccission.md` for the full ADR log behind these choices.
