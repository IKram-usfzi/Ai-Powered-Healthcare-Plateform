# GlobalCare — Enterprise Remote Healthcare Management Platform

**Capstone Project 19 · Diploma in AIOPS (EduQual Level 6) · al-Nafi International College**
**Student:** Ikram Ullah | **Client (fictional, assessment purposes):** GlobalCare Telehealth Network

> Status: **Phases 0–9 complete.** All five PRD modules (Patient/Provider Management, Telemedicine,
> Remote Patient Monitoring, AI Risk Assessment, Executive Dashboard) have working, tested backend
> REST APIs and a full React frontend for the dashboard. Observability (Prometheus/Grafana),
> security (OPA RBAC, Trivy scanning), all 17 mandatory architecture diagrams, and the full
> documentation set (including Installation/Deployment/User/Admin guides) are done and verified
> against real infrastructure. AWS deployment (Phase 8) exists as validated Terraform but is
> deliberately not applied — the real, running deployment is local Docker Compose. Only Phase 10
> (demo/viva rehearsal) remains. See [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) for the detailed,
> continuously-updated phase tracker.

Full project overview, requirements, and documentation index: [`docs/README.md`](./docs/README.md).

## 1. Repository layout

```
/backend        FastAPI application — all 5 modules' REST APIs, SQLAlchemy models + Alembic
                 migration, AI risk classifier (trained model artifact + training script),
                 OPA client, Prometheus instrumentation, seed scripts, pytest suite (77 tests)
/frontend       React + Vite + Tailwind application — JWT login + 3-view Executive Dashboard
                 (Unified/Executive/Operations), built to the supplied "Clinical Precision" template
/infra          Docker Compose (mandatory local deployment: postgres, redis, opa, backend,
                 frontend, prometheus, grafana) + infra/terraform/ (AWS stretch, IaC only)
/docs           Full documentation set (PRD, TRD, architecture, API spec, schema, ADRs, Security,
                 Testing strategy, generated reports, all 4 guides) + docs/diagrams/ (17 mandatory
                 architecture diagrams, Mermaid diagrams-as-code)
/UIUX Design    Supplied 25-screen "Clinical Precision" UI/UX template
mkdocs.yml      MkDocs config, builds the docs/ site (`mkdocs build --strict` — zero warnings)
```

## 2. Quick start

```bash
docker compose -f infra/docker-compose.yml up -d --build
docker compose -f infra/docker-compose.yml exec backend alembic upgrade head
docker compose -f infra/docker-compose.yml exec backend python scripts/seed_dev_users.py
docker compose -f infra/docker-compose.yml exec backend python scripts/seed_synthea.py --patients 200
```

- Frontend: http://localhost:5173 (login: `admin@globalcare-demo.com` / `ChangeMe123!`)
- Backend API docs: http://localhost:8000/docs
- Grafana: http://localhost:3001 (`admin`/`admin`) · Prometheus: http://localhost:9090

Full step-by-step instructions, verification steps, and troubleshooting: [`docs/installation-guide.md`](./docs/installation-guide.md).

## 3. Documentation

Start at [`docs/README.md`](./docs/README.md) for the full documentation index. Most relevant starting points:

- [`docs/installation-guide.md`](./docs/installation-guide.md) — get it running
- [`docs/deployment-guide.md`](./docs/deployment-guide.md) — local (mandatory) and AWS (stretch) deployment profiles
- [`docs/user-guide.md`](./docs/user-guide.md) / [`docs/admin-guide.md`](./docs/admin-guide.md) — how to use it
- [`docs/architecture.md`](./docs/architecture.md) §6 / [`docs/diagrams/`](./docs/diagrams/README.md) — all 17 mandatory diagrams
- [`docs/deccission.md`](./docs/deccission.md) — the full ADR log behind every design decision
- [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) — the continuously-updated phase/task tracker and full session history
