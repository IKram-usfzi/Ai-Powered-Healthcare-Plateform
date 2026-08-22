# GlobalCare — Enterprise Remote Healthcare Management Platform

**Capstone Project 19 · Diploma in AIOPS (EduQual Level 6) · al-Nafi International College**
**Student:** Ikram Ullah | **Client (fictional, assessment purposes):** GlobalCare Telehealth Network

> Status: **Phase 0 (Foundation) in progress.** Documentation set is complete; `backend/`, `frontend/`, and `infra/` now hold a running skeleton (FastAPI health endpoint, React/Vite/Tailwind app, Docker Compose wiring). See root [`README.md`](../README.md) and [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) for current status.

## 1. What this project is

GlobalCare Telehealth Network operates a nationwide digital healthcare platform. This capstone designs, documents, and (in later phases) implements a proof-of-concept **Enterprise Remote Healthcare Management Platform** covering:

- Patient registration & healthcare provider management
- Telemedicine appointments & consultations
- Remote patient monitoring (vitals, abnormal-reading alerts)
- AI-assisted health risk assessment (lightweight ML, decision-support only)
- Executive healthcare operations dashboard

Only simulated/synthetic healthcare data is used — no real patient records or PHI at any point.

## 2. Technology stack (summary)

| Layer | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Frontend | React (UI/UX from a supplied template) |
| Database | PostgreSQL |
| Cache | Redis (dashboard cache, alert de-dup, session/rate-limit) |
| AI/ML | Scikit-learn, Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Containers | Docker, Docker Compose (mandatory); K3s/Kind optional |
| Monitoring | Prometheus, Grafana |
| Security | JWT auth, Open Policy Agent, Trivy |
| Docs | Markdown, MkDocs |
| Diagrams | Mermaid, PlantUML, Draw.io |
| Cloud (stretch) | AWS Free Tier (EC2 + RDS) |

Full rationale in [`TRD.md`](./TRD.md) and [`deccission.md`](./deccission.md).

## 3. Documentation index

| File | Purpose |
|---|---|
| [`PRD.md`](./PRD.md) | Product requirements — problem, users, functional/non-functional requirements |
| [`TRD.md`](./TRD.md) | Technical requirements — stack, environments, compliance, deployment |
| [`architecture.md`](./architecture.md) | System architecture, component breakdown, diagram inventory |
| [`api-spec.md`](./api-spec.md) | API contract — endpoint groups, roles, conventions |
| [`backend-schema.md`](./backend-schema.md) | Database entities, relationships, ERD |
| [`deccission.md`](./deccission.md) | Architecture Decision Records (ADR log) |
| [`developement-rules.md`](./developement-rules.md) | Branching, commit, code-style, and review conventions |
| [`flow.md`](./flow.md) | Key process/workflow and sequence flows |
| [`impmemnentaion-plan.md`](./impmemnentaion-plan.md) | Phased delivery roadmap |
| [`Security.md`](./Security.md) | Security design and standards-compliance mapping |
| [`Testing-startegy.md`](./Testing-startegy.md) | Test levels, AI evaluation approach, coverage |
| [`UIUX.md`](./UIUX.md) | UI/UX reference — pending supplied template |

## 4. Laptop / resource requirements

- Minimum: 8 GB RAM · Recommended: 16 GB RAM (dev machine in use: 16 GB / 512 GB SSD)
- Docker Compose deployment, no GPU required, no distributed clusters
- Kubernetes (K3s/Kind) and Apache Airflow are optional, not required

## 5. Assumptions & limitations

- All healthcare data is synthetic (planned source: Synthea); no real PHI is used or required.
- FHIR/OpenMRS/OpenEMR are addressed conceptually (FHIR-inspired schemas) rather than deployed as running systems, consistent with the exam brief.
- International standards (HL7 FHIR, ISO 27001/27701/42001, NIST AI RMF, NIST CSF 2.0, HIPAA, GDPR, OWASP Top 10, CIS Controls) are addressed as conceptual alignment, not certified compliance.
- AI predictions are decision-support only and always require human clinical judgement.
- An AWS free-tier deployment is an additional stretch goal beyond the exam's mandatory laptop/Docker Compose requirement.

## 6. Future enhancements

- Full AWS free-tier deployment (see `TRD.md` §8 and `impmemnentaion-plan.md` Phase 8)
- Optional K3s/Kind orchestration
- Optional Apache Airflow pipeline for scheduled analytics
- Deeper FHIR interoperability (real HAPI FHIR server) if resources allow

## 7. Testing methodology (summary)

See [`Testing-startegy.md`](./Testing-startegy.md) for the full plan: unit, integration, API, and end-to-end tests, plus AI model evaluation and Trivy-based security scanning.
