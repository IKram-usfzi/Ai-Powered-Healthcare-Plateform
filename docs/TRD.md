# Technical Requirements Document (TRD)

**Related:** `PRD.md`, `architecture.md`, `backend-schema.md`, `Security.md`

## 1. Overview

Technical requirements needed to satisfy the PRD within the exam's laptop-resource constraint, with an additional AWS free-tier deployment as a documented stretch goal.

## 2. Environments

| Environment | Purpose | Notes |
|---|---|---|
| Local dev | Primary development & mandatory exam demo | MacBook, 16 GB RAM / 512 GB SSD; Docker Compose |
| AWS free tier | Stretch/portfolio deployment | EC2 (t2.micro/t3.micro) + RDS PostgreSQL; not required by the exam brief |

## 3. Technology Stack

| Area | Technology | Role |
|---|---|---|
| Language | Python | Backend, AI/ML, data processing, automation |
| Backend | FastAPI | REST APIs, business logic, auth |
| Frontend | React + Tailwind CSS | UI (per supplied "Clinical Precision" template); Tailwind confirmed from the template (ADR-012) |
| Frontend charting | Chart.js | Interactive in-browser dashboard charts, per the template (ADR-012) |
| Frontend type/icons | Manrope + Inter (Google Fonts), Material Symbols Outlined | Confirmed from the template |
| Database | PostgreSQL | System of record (patients, providers, appointments, consultations, readings, alerts, predictions) |
| Cache | Redis | Dashboard KPI cache, alert de-duplication, session/rate-limit state |
| Healthcare standards | HAPI FHIR / OpenMRS / OpenEMR | Conceptual reference only (FHIR-inspired schemas in FastAPI) |
| ML | Scikit-learn | Lightweight classification (health risk categories) |
| Data | Pandas, NumPy | Preprocessing, numerical operations |
| Visualization | Plotly, Matplotlib | Dashboards and analytics charts |
| Workflow automation | Apache Airflow | Optional, only if it adds real POC value |
| Containers | Docker, Docker Compose | Mandatory packaging & deployment |
| Orchestration | K3s / Kind | Optional stretch |
| Monitoring | Prometheus, Grafana | Metrics collection & visualization |
| Security | Trivy, OPA, JWT | Scanning, policy-based RBAC, authentication |
| VCS | Git, GitHub | Version control, portfolio hosting |
| Docs | Markdown, MkDocs | Documentation site |
| Diagrams | Draw.io, PlantUML, Mermaid | Architecture/flow diagrams (Mermaid/PlantUML preferred for diagrams-as-code) |
| Cloud (stretch) | AWS (EC2, RDS, VPC, CloudFront) | Free-tier deployment |

## 4. Data Requirements

- Primary synthetic data source: **Synthea** (MITRE) — FHIR R4-shaped synthetic patients, reinforcing the conceptual-FHIR approach.
- Optional supplementary source: a flatter Kaggle synthetic vitals dataset for AI model training, if Synthea's structure needs augmenting.
- No real PHI is imported, stored, or processed at any stage.

## 5. Integration Requirements

- React ↔ FastAPI over REST, JWT bearer auth.
- FastAPI ↔ PostgreSQL via an ORM (tooling choice deferred to implementation phase).
- FastAPI ↔ Redis for caching/rate-limiting/alert de-dup.
- FastAPI metrics ↔ Prometheus (scrape endpoint) ↔ Grafana (dashboards).
- FastAPI ↔ OPA for policy-based authorization decisions.
- Docker images ↔ Trivy for vulnerability scanning in the build/deploy process.

## 6. Performance Requirements

- Responsive interaction on an 8–16 GB laptop with no GPU.
- API endpoints should return promptly for demo-scale synthetic data volumes (exact SLAs deferred to implementation/testing phase — see `Testing-startegy.md`).

## 7. Scalability Considerations

Not a primary requirement for this proof-of-concept, but the layered architecture (stateless API + managed DB) keeps a path open toward horizontal scaling (e.g., via K3s or AWS Auto Scaling) as a future enhancement.

## 8. Deployment Requirements

**Mandatory:** Docker Compose on a standard student laptop (per exam brief §4/§11).

**Stretch (AWS Free Tier):**
- VPC with public subnet (EC2 running Docker Compose for FastAPI/React/Redis) and private subnet (RDS PostgreSQL).
- Security groups restricting inbound traffic to required ports only.
- AWS Budgets billing alarm configured before any deployment activity.
- Note: AWS restructured its Free Tier on 15 July 2025. Accounts created after that date receive a ~$100–200 credit (6-month window) rather than 12 months of separately-free EC2/RDS hours; legacy accounts keep the older always-free-for-12-months model. Confirm which applies before relying on "free" capacity.
- Given ~1 GB RAM on a t2/t3.micro instance, Prometheus/Grafana run in a trimmed or demo-only capacity on this profile; PostgreSQL is offloaded to RDS to conserve instance memory.

## 9. Compliance & Standards Requirements (conceptual alignment)

HL7 FHIR, DICOM (conceptual), ISO 13131 (Telehealth), ISO 15189 (conceptual), ISO 13485 (conceptual), ISO/IEC 27001, ISO/IEC 27701, ISO/IEC 42001, NIST AI RMF, NIST Cybersecurity Framework 2.0, HIPAA (conceptual), GDPR (conceptual), OWASP Top 10, CIS Critical Security Controls. Full mapping in `Security.md`.

## 10. Monitoring & Observability Requirements

Prometheus scrapes FastAPI metrics (CPU, memory, request count/latency, error count); Grafana visualizes them on a dashboard. Full monitoring runs on the local/full profile; trimmed on the AWS free-tier profile.

## 11. Security Requirements

See `Security.md` for authentication, authorization, data protection, secrets management, network security, and audit-logging requirements.
