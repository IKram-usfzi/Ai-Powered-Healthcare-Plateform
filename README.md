# GlobalCare — Enterprise Remote Healthcare Management Platform

**Capstone Project 19 · Diploma in AIOPS (EduQual Level 6) · al-Nafi International College**
**Student:** Ikram Ullah | **Client (fictional, assessment purposes):** GlobalCare Telehealth Network

> Status: **Phase 2 (Module 1 — Patient & Provider Management) done.** JWT-authenticated REST API
> for patients/providers/facilities/registration reporting, backed by a real database schema and
> Synthea-derived seed data. See §3 below.

Full project overview, requirements, and documentation index: [`docs/README.md`](./docs/README.md).

## 1. Repository layout

```
/backend        FastAPI application — auth, patients/providers/facilities/reports (Phase 2),
                 SQLAlchemy models + Alembic migration (Phase 1), Synthea seed scripts, pytest suite
/frontend       React + Vite + Tailwind application (Phase 0 skeleton)
/infra          Docker Compose setup wiring backend, frontend, PostgreSQL, Redis
/docs           Full documentation set (PRD, TRD, architecture, API spec, schema, ADRs, ...)
/diagrams       Mermaid/PlantUML diagram sources (Phase 9)
/UIUX Design    Supplied 25-screen "Clinical Precision" UI/UX template
mkdocs.yml      MkDocs config, builds the docs/ site
```

## 2. Quick start

```bash
cd infra
docker compose up --build
```

- Backend: http://localhost:8000/docs (FastAPI/Swagger)
- Frontend: http://localhost:5173

See [`infra/README.md`](./infra/README.md) for details.

## 3. Current status

See [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) for the up-to-date phase/task tracker, and
[`docs/impmemnentaion-plan.md`](./docs/impmemnentaion-plan.md) for the full 10-phase roadmap.

## 4. Documentation

Start at [`docs/README.md`](./docs/README.md) for the full documentation index (PRD, TRD,
architecture, API contract, database schema, ADRs, dev conventions, security, testing strategy,
UI/UX spec).
