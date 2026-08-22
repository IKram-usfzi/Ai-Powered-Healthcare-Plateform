# Project Context

> Read this file first, every session. It is project memory, not documentation — for depth, follow the file paths under each section into `docs/`.

## 1. Project Identity

- **Project name:** GlobalCare — Enterprise Remote Healthcare Management Platform (GitHub repo: `Ai-Powered-Healthcare-Plateform`)
- **Project type:** Academic capstone (Diploma in AIOPS, EduQual Level 6, al-Nafi International College) — built as a real proof-of-concept enterprise web platform, not a toy exercise
- **Project purpose:** Design, document, and build a proof-of-concept healthcare platform for a fictional client, "GlobalCare Telehealth Network," to pass a 3-stage exam (presentation, live demo + GitHub review, viva voce)
- **Current development stage:** Phases 0-6 done and verified against real Docker Compose + PostgreSQL + Redis (2026-08-22). All five PRD modules have working, tested backend REST APIs — 72 passing pytest tests plus live end-to-end verification against real infrastructure for every phase. Phase 6 also delivered the first real frontend: JWT login plus three routed React dashboard views (Unified, Executive Overview, Healthcare Operations) built to the "Clinical Precision" template and verified with real seeded data via browser automation. Phase 7 (Observability/Security) is next.
- **Main objective:** A Docker-Compose-deployable platform (5 functional modules) + a complete documentation set + 17 required architecture diagrams, defensible live in front of an examiner.

## 2. Project Summary

GlobalCare is a fictional nationwide telehealth network with 8M+ (simulated) patients. Its systems are fragmented — clinicians can't get a unified view of patients, appointments, monitoring alerts, or analytics. This project designs and will build a single Enterprise Remote Healthcare Management Platform covering patient/provider registration, telemedicine scheduling and consultations, remote vitals monitoring with alerting, a lightweight AI health-risk classifier, and an executive operations dashboard. It runs via Docker Compose on a student laptop (8–16 GB RAM, no GPU) as the mandatory deliverable, with an AWS free-tier deployment as an optional stretch goal. Only synthetic data is used — no real PHI. The project is currently 100% in the documentation/architecture phase; zero backend or frontend code exists yet.

## 3. Problem Being Solved

Fragmented systems for registration, scheduling, telemedicine, and monitoring leave clinicians switching between tools with no centralized view, inconsistent monitoring alerts, and no operational analytics.
Detailed requirements: `docs/PRD.md` §3 · Original exam brief: student's local copy, not in this repo (see §17 below)

## 4. Solution Overview

Five modules, all behind one React frontend and one FastAPI backend:
1. Patient & provider registration/management
2. Telemedicine appointment scheduling & consultations
3. Remote patient monitoring (vitals + abnormal-reading alerts)
4. AI-assisted health risk assessment (lightweight classifier, decision-support only)
5. Executive Healthcare Operations Dashboard (implemented as 3 cooperating views — see `docs/UIUX.md` §3)

Detailed solution scope: `docs/PRD.md` §6–7

## 5. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python | Backend, AI/ML, data processing |
| Backend | FastAPI | REST APIs, business logic, auth |
| Frontend | React + Tailwind CSS | UI, per the supplied "Clinical Precision" template |
| Frontend charting | Chart.js | Interactive dashboard charts |
| Database | PostgreSQL | System of record |
| Cache | Redis | Dashboard cache, alert de-dup, session/rate-limit |
| AI/ML | Scikit-learn, Pandas, NumPy | Health risk classification |
| Containers | Docker, Docker Compose | Mandatory deployment (K3s/Kind optional) |
| Monitoring | Prometheus, Grafana | Metrics/observability |
| Security | JWT, Open Policy Agent, Trivy | AuthN/RBAC/image scanning |
| Docs | Markdown, MkDocs | Documentation site (not yet built) |
| Diagrams | Mermaid, PlantUML, Draw.io | Architecture-diagrams-as-code |
| Cloud (stretch, optional) | AWS Free Tier (EC2 + RDS) | Not required by the exam brief |

Full rationale: `docs/TRD.md`, `docs/deccission.md`

## 6. Architecture

```
User (Patient / Doctor / Admin / Executive)
        ↓
React + Tailwind Frontend
        ↓
FastAPI Backend (auth, business logic)
        ↓
PostgreSQL (system of record) + Redis (cache) + AI service (Scikit-learn)
```

Cross-cutting: JWT+OPA auth, Trivy scanning, Prometheus/Grafana monitoring — all layered on Docker Compose.
Detailed architecture (incl. AWS stretch topology, 17-diagram inventory): `docs/architecture.md`

## 7. Core Modules

| Module | Purpose | Status |
|---|---|---|
| Patient & Provider Management | Registration, profiles, facility/provider assignment | BACKEND API DONE (Phase 2) — surfaced via the Phase 6 dashboards, no dedicated CRUD UI yet |
| Telemedicine Appointments | Scheduling, consultations, status tracking | BACKEND API DONE (Phase 3) — surfaced via the Phase 6 dashboards, no dedicated CRUD UI yet |
| Remote Patient Monitoring | Vitals ingestion, abnormal-reading alerts | BACKEND API DONE (Phase 4) — surfaced via the Phase 6 dashboards, no dedicated CRUD UI yet |
| AI Health Risk Assessment | Lightweight classifier, confidence-scored predictions | BACKEND API DONE (Phase 5) — surfaced via the Phase 6 dashboards, no dedicated CRUD UI yet |
| Executive Operations Dashboard | 3-view KPI/ops dashboard (Unified/Executive/Operations) | DONE (Phase 6) — backend aggregation + full React frontend, verified against real data |

All five are fully specified in `docs/PRD.md`, `docs/api-spec.md`, `docs/backend-schema.md`, and all five have working, verified backend APIs as of Phase 6. The Executive Dashboard is the only module with a full dedicated frontend so far — the other four modules' data is visible through the dashboards (patients, appointments, alerts, predictions all appear as real aggregated figures) but don't yet have their own dedicated management screens (e.g. no patient-list/registration-form UI); that remains future/stretch work beyond the mandatory Phase 6 scope.

## 8. Current Implementation Status

**Completed and pushed to GitHub** (`github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform`, `main`):
- Full documentation set (12+ files: PRD, TRD, architecture, api-spec, backend-schema, deccission/ADR log, developement-rules, flow, impmemnentaion-plan, Security, Testing-startegy, UIUX, test-execution-log) and the 25-screen UI/UX template under `UIUX Design/`.
- **Phase 0 — Foundation:** `backend/` (FastAPI skeleton), `frontend/` (React+Vite+Tailwind skeleton), `infra/docker-compose.yml`, root `README.md`, `mkdocs.yml`. Verified: FastAPI health endpoint runs; `mkdocs build --strict` clean; frontend+backend later confirmed running together (see below).
- **Phase 1 — Data & Domain Modeling:** 9 SQLAlchemy models matching `backend-schema.md`, Alembic migration, `fetch_synthea.py`/`seed_synthea.py`. Verified: migration up/down clean on SQLite; seed script loads 200 patients/50 facilities/50 providers/953 health_readings with real Synthea vitals + physiologically-plausible simulated SpO2/temperature.
- **Phase 2 — Module 1 (Patient & Provider Management):** JWT auth (`app/core/security.py`, `app/api/deps.py`) + all `api-spec.md` §2-3 endpoints (`/auth/*`, `/patients`, `/providers`, `/facilities`, `/reports/registration`), with role-based access control including the doctor-scoped "assigned patients only" rule and patient self-access. Ruff+Black clean.
- **Real Docker Compose + PostgreSQL verification (2026-08-22)** — see §17 item 7 for the critical context (the user's "own machine" turned out to be this same sandbox). `docker compose up -d` (postgres+redis+backend+frontend) all healthy; `alembic upgrade head` applied against real Postgres; `seed_dev_users.py` + `seed_synthea.py` loaded real data; a real login returned a valid JWT. **Independently confirmed by Claude directly** (not just relying on the user's paste-backs) via `sg docker -c "docker ..."`: fetched the live `/openapi.json` (all 10 endpoints present) and queried the real Postgres database directly (200 patients, 50 providers, 50 facilities, 953 health_readings, 52 users — exact expected counts). This closes the "SQLite-verified, Postgres-pending" caveat that had applied to every phase. Two real bugs were caught and fixed by this real-infra run — see next bullet.
- ADR-016 through ADR-019 (blood pressure split, Synthea-only confirmed, `assigned_provider_id` added to close an api-spec/schema gap, all timestamps made timezone-aware) — found during implementation/verification. Two more real bugs found by the *Docker* run specifically (not caught by SQLite testing): (a) `backend/Dockerfile` never learned to copy `alembic.ini`/`alembic/`/`scripts/` when those were added in Phase 1-2 — fixed, plus a related fix so the Synthea data path resolves correctly via a `SYNTHEA_DATA_DIR` env var + bind mount; (b) `bcrypt` was unpinned in `requirements.txt` and pip resolved a version incompatible with `passlib==1.7.4` inside the fresh Docker build (worked in the authoring sandbox only by luck, on an old cached bcrypt) — fixed by pinning `bcrypt==4.0.1`. Full details: `docs/test-execution-log.md`.
- **Phase 3 — Module 2 (Telemedicine Appointment & Consultation):** all `api-spec.md` §4 endpoints (`/appointments` POST/GET, `/appointments/{id}/status` PATCH, `/consultations` POST, `/consultations/{patientId}` GET, `/providers/{id}/schedule` GET, `/reports/appointments` GET). Recording a consultation auto-completes its appointment. Verified two ways: 10 new pytest tests (suite now 34/34 passing) and a live Docker Compose + PostgreSQL walkthrough (restarted the backend container to pick up the bind-mounted code, no rebuild needed) — book → doctor login → view schedule → update status → record consultation → history → report → role-denial check, all correct, response bodies inspected directly. No new bugs found this time — everything worked on the first try. Full details: `docs/test-execution-log.md`.
- **Phase 4 — Module 3 (Remote Patient Monitoring):** all `api-spec.md` §5 endpoints (`/monitoring/readings` POST/GET, `/monitoring/alerts` GET, `/monitoring/alerts/{id}/acknowledge` PATCH). Threshold-based severity detection (`app/services/vitals.py`, 3 tiers across all 5 vitals). **Redis is now actually wired in** (`app/core/redis_client.py`) — running in Docker Compose since Phase 0 but unused until now — for the exact de-dup role ADR-002 scoped it to: a 5-minute per-patient key stops repeated abnormal readings from spamming duplicate alerts. Found and fixed ADR-020 first (`PatientCreate` had no way to create a linked login — no patient could ever exercise "self" access at all, including this phase's own endpoints; fixed by adding optional `email`/`password`, mirroring `ProviderCreate`). Verified two ways: 12 new pytest tests (suite now 53/53) including the literal exit-criteria scenario, plus a live run against **real Redis** (not the test suite's in-memory fake) — 3 abnormal readings produced exactly 1 alert. Full details: `docs/test-execution-log.md`.
- **Phase 5 — Module 4 (AI-Assisted Health Risk Assessment):** all `api-spec.md` §6 endpoints (`POST /ai/risk-assessment`, `GET /ai/predictions/{patientId}`, `GET /ai/model/metadata`). Added pandas/numpy/scikit-learn/joblib. `scripts/train_risk_model.py` builds a training set from all 957 real `health_readings` rows, labels them via a weighted point-score heuristic (ADR-021, deliberately different from Module 3's alert-threshold logic so the classifier isn't just trivially replicating existing code), and trains a `RandomForestClassifier` — real measured accuracy/precision/recall/F1 written to `docs/ai-evaluation-report.md` (new). Feature extraction is shared verbatim between training and inference (`app/services/risk_features.py`) to avoid train/serve skew. Found and fixed a second occurrence of the exact Phase 1 `SYNTHEA_DATA_DIR` bug class: the evaluation report's write path resolved to a container-only location until a `DOCS_DIR` env var + `../docs:/docs` bind mount were added (see §17 item 11 — this is now a recognized recurring bug pattern, not a one-off). Verified two ways: 12 new pytest tests (suite now 65/65), and a live Docker Compose + PostgreSQL run — patient submits vitals → doctor runs an assessment → prediction stored with category/confidence/recommendation → prediction history (doctor + patient self) → model metadata (admin) → role-denial check, all correct. Full details: `docs/test-execution-log.md`.
- **Phase 6 — Module 5 (Executive Healthcare Operations Dashboard):** backend — `GET /dashboard/overview`, `GET /dashboard/trends`, `GET /dashboard/provider-activity`, `GET /reports/executive` (`app/api/v1/dashboard.py`, `app/schemas/dashboard.py`), all real SQL aggregation, no fabricated figures. Frontend — the first real UI work since the Phase 0 placeholder: JWT login (`/login`) plus three routed, role-gated React views matching the "Clinical Precision" template exactly — Unified home (`/dashboard`), Executive Overview with a live Chart.js trend line (`/dashboard/executive`, Executive-only), Healthcare Operations (`/dashboard/operations`). Wherever the template assumed untracked data (bed occupancy, no-show rate, provider presence/load), substituted a real computable equivalent instead (ADR-022, `docs/UIUX.md` §5 "honest data only"). Verified two ways: 7 new pytest tests (suite now 72/72), ruff+black clean; and a live Docker Compose + PostgreSQL + frontend run via browser automation with 204 real seeded patients — logged in as both `administrator` and `executive` demo users, confirmed all three views render correct real data, confirmed `ProtectedRoute` correctly redirects an administrator away from the executive-only route, confirmed the Executive-only "Export Data" button downloads the real JSON report. Found and fixed three real bugs: a `tailwind.config.js`/`postcss.config.js`/`eslint.config.js` Docker bind-mount gap (ADR-023, same bug class as `SYNTHEA_DATA_DIR`/`DOCS_DIR`, this time for dev tooling), a stale backend container after adding `appointments_today_by_status` (uvicorn runs without `--reload`), and an ESLint config missing browser globals + JSX-usage detection (fixed by adding `globals.browser` and `eslint-plugin-react`'s recommended rules). Full details: `docs/test-execution-log.md`.

**In Progress:** Nothing actively mid-implementation.

**Not Started:**
- Phase 7 (Observability/Security — OPA/Prometheus/Grafana/Trivy), Phase 8 (AWS, stretch), Phase 9 (the 17 mandatory diagrams as actual files), Phase 10 (formal testing/demo prep)
- AWS budget alarm status — unknown, unverified

**Blocked:** None currently. Direct git push from this sandbox works once the user supplies a GitHub token (confirmed multiple times this session) — see §17 item 3.

## 9. Current Development Phase

Phases (from `docs/impmemnentaion-plan.md`):
Phase 0 — Foundation · Phase 1 — Data & Domain Modeling · Phase 2 — Module 1 (Patients/Providers) · Phase 3 — Module 2 (Telemedicine) · Phase 4 — Module 3 (Monitoring) · Phase 5 — Module 4 (AI Risk) · Phase 6 — Module 5 (Dashboard) · Phase 7 — Observability/Security · Phase 8 — AWS (stretch) · Phase 9 — Docs/Diagrams · Phase 10 — Testing/Demo Prep

**CURRENT PHASE: Phase 6 — Module 5: Executive Healthcare Operations Dashboard (DONE, fully verified against real Docker Compose + PostgreSQL + live browser automation).** All backend aggregation endpoints implemented; all three frontend dashboard views built to the "Clinical Precision" template and verified rendering real data as both `administrator` and `executive` demo users; 72/72 pytest tests passing; `npm run lint` clean. Three real bugs found and fixed during verification (dev-tooling Docker bind-mount gap, stale backend container, broken ESLint config) — see §8 and ADR-022/ADR-023.

## 10. Current Task

```
CURRENT TASK:
Commit and push Phase 6, then start Phase 7 (Observability & Security
Hardening).

OBJECTIVE:
Prometheus metrics instrumentation, Grafana dashboards, OPA policy
authoring, Trivy scans wired into the build process, per docs/Security.md
and impmemnentaion-plan.md Phase 7.

STATUS:
Phase 5 (ac851b0) is pushed. Phase 6 work (dashboard backend + full React
frontend) is complete and verified but NOT YET COMMITTED as of this note.

FILES TO COMMIT NEXT (Phase 6):
backend/app/schemas/dashboard.py (new), backend/app/api/v1/dashboard.py
(new), backend/app/api/v1/reports.py (+/reports/executive), router.py
(wired dashboard router), backend/tests/test_dashboard.py (new),
infra/docker-compose.yml (+tailwind/postcss/eslint config bind mounts),
frontend/tailwind.config.js (full design tokens), frontend/src/index.css
(+glass-card/status-pill utilities), frontend/eslint.config.js (fixed
browser globals + JSX-usage detection), frontend/src/api/ (new),
frontend/src/auth/ (new), frontend/src/components/ (new),
frontend/src/pages/ (new), frontend/src/App.jsx + main.jsx (real routing,
replacing the Phase 0 placeholder), docs/deccission.md (+ADR-022,
ADR-023), docs/impmemnentaion-plan.md (Phase 6 status),
docs/test-execution-log.md (+Phase 6 section), docs/UIUX.md (§5 Open
Items resolved), PROJECT_CONTEXT.md (this file).

EXPECTED RESULT:
Commit pushed to github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform main.
```

## 11. NEXT STEPS

1. Commit and push Phase 6 (needs the user's GitHub token or the user pushing themselves — see §17 item 3)
2. Start Phase 7: Observability & Security Hardening — Prometheus, Grafana, OPA, Trivy, per `docs/Security.md`
3. Consider dedicated management UIs (patient list, appointment booking, etc.) as future/stretch work — not required by the exam brief, which only mandates the dashboard for the frontend (§4 module 5)

```
NEXT IMMEDIATE ACTION:
Commit Phase 6 and push (pending token/user push), then begin Phase 7:
Prometheus/Grafana metrics + OPA policies + Trivy scanning per
docs/Security.md.
```

## 12. Project Roadmap

**Phase 0 — Foundation**
- [x] Repository created, pushed to GitHub
- [x] README, ADR log (`deccission.md`)
- [x] `backend/` / `frontend/` / `infra/` folder skeleton
- [x] `docker-compose.yml` — **verified with real `docker compose up`** (postgres+redis+backend+frontend, all healthy)
- [x] `.gitignore` strengthened beyond `*.pdf`
- [x] MkDocs initialized (`mkdocs build --strict` verified locally)
- [x] Phase 0 scaffolding committed/pushed to GitHub (commit `367b98b`)
- [ ] AWS budget alarm — status UNKNOWN, needs verification

**Phase 1 — Data & Domain Modeling**
- [x] PostgreSQL schema as real SQLAlchemy models + Alembic migration — **verified against real PostgreSQL** (`alembic upgrade head` in Docker Compose)
- [x] Synthea dataset pulled/generated and mapped (`fetch_synthea.py`/`seed_synthea.py`) — **verified loaded into real Postgres**: 200 patients/50 facilities/50 providers/953 health_readings, confirmed via direct SQL query
- [x] Phase 1 work committed/pushed to GitHub (commit `9ba98b2`)

**Phase 2 — Module 1: Patient & Provider Management**
- [x] JWT auth (`/auth/login`, `/auth/refresh`, `/auth/me`) — **verified: real login against Postgres returned a valid JWT**
- [x] Patients/Providers/Facilities CRUD per `api-spec.md` §3
- [x] Role model + doctor-scoped/patient-self-access authorization
- [x] Registration report (`/reports/registration`)
- [x] 24 automated pytest tests, all passing; manual E2E curl walkthrough verified; **real Docker Compose + PostgreSQL run verified** (all 10 endpoints live, confirmed via `/openapi.json`)
- [x] Phase 2 work committed/pushed to GitHub (commit `5206032`)
- [x] Dockerfile/bcrypt fixes from the real Docker run committed/pushed (commit `a503a75`)

**Phase 3 — Module 2: Telemedicine Appointment & Consultation**
- [x] Appointments CRUD + status updates per `api-spec.md` §4
- [x] Consultations (record + history), auto-completes the appointment
- [x] Provider schedule endpoint
- [x] Appointment/operational report (`/reports/appointments`)
- [x] 10 new pytest tests (suite now 34/34); real Docker Compose + PostgreSQL walkthrough verified
- [x] Phase 3 work committed/pushed to GitHub (commit `f24884a`)

**Phase 4 — Module 3: Remote Patient Monitoring**
- [x] Vitals ingestion (`POST /monitoring/readings`, Patient self-submission)
- [x] Reading history (`GET /monitoring/readings/{patientId}`)
- [x] Threshold-based abnormal detection (3 severity tiers, `app/services/vitals.py`)
- [x] Alerts: list (`GET /monitoring/alerts`) + acknowledge (`PATCH .../acknowledge`)
- [x] Redis actually wired in for alert de-dup (first real use since Phase 0)
- [x] ADR-020: `PatientCreate` gains optional login (patients could not log in at all before this)
- [x] 12 new pytest tests (suite now 53/53); real Docker Compose + PostgreSQL + **real Redis** verified — exit criteria (3 abnormal readings → 1 alert) confirmed against real infra, not just the test fake
- [x] Phase 4 work committed/pushed to GitHub (commit `42a587c`)

**Phase 5 — Module 4: AI-Assisted Health Risk Assessment**
- [x] Risk assessment (`POST /ai/risk-assessment`, Doctor-only, assigned patients)
- [x] Prediction history (`GET /ai/predictions/{patientId}`)
- [x] Model metadata (`GET /ai/model/metadata`, Administrator-only)
- [x] RandomForestClassifier trained on real seeded data (957 readings), real measured metrics (ADR-021)
- [x] `docs/ai-evaluation-report.md` generated (Testing-startegy.md §3 deliverable)
- [x] 12 new pytest tests (suite now 65/65); real Docker Compose + PostgreSQL walkthrough verified
- [x] Phase 5 work committed/pushed to GitHub (commit `ac851b0`)

**Phase 6 — Module 5: Executive Healthcare Operations Dashboard**
- [x] Dashboard aggregation endpoints (`/dashboard/overview`, `/dashboard/trends`, `/dashboard/provider-activity`, `/reports/executive`)
- [x] JWT login UI + role-gated routing (`ProtectedRoute`)
- [x] Three dashboard views built to the "Clinical Precision" template: Unified, Executive Overview (Chart.js trend line), Healthcare Operations
- [x] "Honest data only" substitutions for untracked template metrics (ADR-022)
- [x] 7 new pytest tests (suite now 72/72); `npm run lint` clean; real Docker Compose + PostgreSQL + browser-automation walkthrough verified as both administrator and executive
- [ ] Phase 6 work committed/pushed to GitHub — pending token/user push

**Phase 7 — Observability & Security**
- [ ] Not started

**Phase 8 — AWS Deployment (stretch, optional)**
- [ ] Not started

**Phase 9 — Documentation & Diagrams**
- [x] Written documentation (12 files)
- [ ] 17 mandatory diagrams as actual diagram files (currently prose-only)
- [ ] MkDocs site built

**Phase 10 — Testing & Demo Prep**
- [ ] Not started

## 13. Important Decisions

Full ADR log: `docs/deccission.md`. Key ones that constrain future work:

- **FastAPI + PostgreSQL + Redis(scoped) + React/Tailwind/Chart.js** as the confirmed stack — ADR-001, ADR-002, ADR-012
- **FHIR conceptual alignment only** — do not deploy a real HAPI FHIR/OpenMRS/OpenEMR server — ADR-003
- **Docker Compose is mandatory**; AWS is an optional, non-required stretch — ADR-004
- **Synthea (MITRE) is the primary synthetic data source** — ADR-005, ADR-011 (supplementary Kaggle dataset still open)
- **JWT + narrowly-scoped OPA policies** for RBAC, not a general policy platform — ADR-006
- **UI/UX comes from the supplied "Clinical Precision" template** — do not design UI independently — ADR-010
- **Dashboard = 3 cooperating views** (Unified/Executive/Operations), not one screen — see `docs/UIUX.md` §3 (routing resolved: `/dashboard`, `/dashboard/executive`, `/dashboard/operations`)
- **Dashboard KPIs never fabricate untracked template metrics** (bed occupancy, no-shows, presence indicators) — substitute a real computable equivalent instead — ADR-022
- **Frontend dev-tooling config files (`tailwind.config.js`, `postcss.config.js`, `eslint.config.js`) are bind-mounted in Docker Compose**, not baked into the image — edit-and-recreate, not rebuild — ADR-023

## 14. Non-Negotiable Constraints

- Must run on 8–16 GB RAM via Docker Compose (mandatory exam requirement) — no GPU, no distributed clusters, no locally-hosted LLMs, no Apache Spark
- No real patient data / PHI — synthetic data only
- Do not deploy HAPI FHIR/OpenMRS/OpenEMR as running services — conceptual alignment only
- AI output is decision-support only — always requires human clinical judgement, never framed as diagnosis
- UI must follow the supplied template — do not design new UI/UX independently
- Kubernetes (K3s/Kind) and Apache Airflow are optional — do not make them required dependencies
- AWS deployment is a stretch goal, not a requirement — never let it block the mandatory Docker Compose deliverable

## 15. Important Files

| Path | Purpose |
|---|---|
| `docs/README.md` | Project overview (note: not at repo root — see §17) |
| `docs/PRD.md` | Product requirements |
| `docs/TRD.md` | Technical requirements |
| `docs/architecture.md` | System architecture + diagram inventory |
| `docs/api-spec.md` | API contract |
| `docs/backend-schema.md` | Database entities/ERD (design-level) |
| `docs/deccission.md` | ADR log |
| `docs/developement-rules.md` | Branching/commit/code-style conventions |
| `docs/flow.md` | Process/sequence flows |
| `docs/impmemnentaion-plan.md` | Phased roadmap (source for §9–12 above) |
| `docs/Security.md` | Security design + standards mapping |
| `docs/Testing-startegy.md` | Test strategy |
| `docs/UIUX.md` | Design system + full Dashboard spec + 25-screen inventory |
| `UIUX Design/` | Raw supplied template: `DESIGN.md`/`DESIGN2.md` (design systems) + `s1`–`s25` (each: `code.html`, `DESIGN.md`, `screen.png`) |
| `technology_stack.txt` | Original raw tech-stack briefing from the student's program |
| `.gitignore` | Currently only excludes `*.pdf` — needs strengthening, see §17 |
| `backend/`, `frontend/`, `infra/` | **Do not exist yet** — first thing to create (§10–11) |

## 16. Documentation Map

- Requirements → `docs/PRD.md`
- Technical requirements → `docs/TRD.md`
- Architecture → `docs/architecture.md`
- API contract → `docs/api-spec.md`
- Database schema → `docs/backend-schema.md`
- Decisions (ADRs) → `docs/deccission.md`
- Dev conventions → `docs/developement-rules.md`
- Process flows → `docs/flow.md`
- Roadmap/phases → `docs/impmemnentaion-plan.md`
- Security → `docs/Security.md`
- Testing → `docs/Testing-startegy.md`
- UI/UX (design system + dashboard spec) → `docs/UIUX.md`

## 17. Known Issues / Risks

**1. `.gitignore` is too weak for what's coming next** — RESOLVED this session
STATUS: Fixed — `.gitignore` now covers Python (`__pycache__/`, `.venv/`, etc.), Node (`node_modules/`, build dirs), `.env`/`.env.*` (with `.env.example` allow-listed), MkDocs `site/`, and OS/editor cruft. NEXT ACTION: None — re-check if a new tool/language is added later.

**2. No root-level `README.md`** — RESOLVED this session
STATUS: Fixed — root `README.md` created, points into `docs/README.md` for the full index. NEXT ACTION: None.

**3. Direct git push from this sandbox needs a user-supplied token — otherwise it's blocked**
STATUS: Well-established this session — pushed successfully 3 times using `git push https://<user>:<token>@github.com/...` (no `-u`, so the token is never written to `.git/config`; confirmed clean after every push). Without a token, an earlier session hit a sandbox git-proxy rejection ("not in this session's authorized repository set"). IMPACT: Low — just ask the user for a token each session/whenever the previous one might be stale; they've supplied the same token 3 times across this session without rotating it despite being advised to. NEXT ACTION: Always ask for a token before attempting to push; never assume one from a prior turn is still available (this code doesn't persist secrets between turns) or still valid.

**4. Cloud sandbox local clones go stale**
STATUS: Confirmed — an earlier local clone in a prior session diverged from what the user actually pushed (different file set/commit). IMPACT: Medium — future sessions must `git fetch && git reset --hard origin/main` (after checking for uncommitted work) before trusting the local tree, never assume the local sandbox clone is current. NEXT ACTION: Standard practice for every new session (see §19).

**5. Several design decisions still open**
STATUS: Mostly resolved. (a) Synthea-only vs. + supplementary Kaggle vitals dataset (ADR-011) — RESOLVED as ADR-017 (Synthea only). (b) Dashboard routing — RESOLVED this session (Phase 6): 3 explicit routes (`/dashboard`, `/dashboard/executive`, `/dashboard/operations`), not a role-based single-route default — see `docs/UIUX.md` §5 and `PROJECT_CONTEXT.md` §13. (c) `UIUX Design/s22` (Documents) and `s25` (Patient Mobile App) — RESOLVED as out of scope; neither is a mandatory module and Phase 6 did not build them. Still open: (d) AWS account creation date (pre/post 15 Jul 2025) — determines which AWS Free Tier model applies, unknown/unverified. NEXT ACTION: Resolve (d) before Phase 8 (AWS, stretch) begins.

**6. AWS budget alarm status**
STATUS: UNKNOWN — needs verification. Phase 0's exit criteria calls for one; not confirmed done or not done. NEXT ACTION: Verify before any AWS work (Phase 8) begins.

**7. This sandbox has no Docker, no PostgreSQL, and no passwordless sudo. Node/npm and pip are NOT pre-installed but CAN be obtained without sudo (portable binaries) — do this at the start of any session that needs them, don't assume they're still there from a prior session.**
STATUS: MOSTLY OBSOLETE as of 2026-08-22 — see the critical correction in item 10 below (**the user's terminal and this sandbox are the same machine**). Docker is now installed here (the user ran `sudo apt install docker.io docker-compose-v2`) and PostgreSQL runs fine as a container. Node/pip were already confirmed obtainable without sudo (portable binaries) earlier in the session — that part still stands. What remains true: no *passwordless* sudo (the user has the password and types it interactively; Claude does not and should not try to obtain it). IMPACT: None now for Docker/Postgres verification — both are fully available. NEXT ACTION: At the start of a future session, check `docker ps` / `sg docker -c "docker ps"` before assuming Docker is unavailable — it may already be installed from this session. If a fresh sandbox genuinely has none of this (Docker, Node, pip), the original acquisition steps in this item's history still apply: get-pip.py --user for pip, the nodejs.org portable tarball for Node, `sudo apt install docker.io docker-compose-v2` for Docker (ask the user to run the sudo-gated step themselves, or if Claude and the user share a terminal, ask the user to run it and then Claude can access it via `sg docker -c "..."` once the docker group exists — no sudo needed for that part).

**11. Recurring bug pattern: scripts that navigate `Path(__file__).resolve().parent...N times...` to reach something outside `backend/` break inside Docker, silently**
STATUS: Confirmed twice now — Phase 1's `SYNTHEA_DATA_DIR` (fetch_synthea.py/seed_synthea.py reaching for `<repo-root>/data/`) and Phase 5's `DOCS_DIR` (train_risk_model.py reaching for `<repo-root>/docs/`). Root cause: locally, a script at `backend/scripts/foo.py` is 3 `.parent`s away from the repo root (`scripts → backend → repo-root`); inside the Docker image, `WORKDIR /app` **is** `backend/`'s contents directly (the Dockerfile does `COPY app ./app` etc., not `COPY backend ./backend`), so the same 3-`.parent` navigation from `/app/scripts/foo.py` lands at `/` (container root) instead of the repo root — silently creating/reading the wrong path, no error, just wrong data or a lost file. IMPACT: Medium — each occurrence looked like it worked (script ran, printed a success message) until someone checked whether the output actually landed on the host. NEXT ACTION: Any NEW script added under `backend/scripts/` that reads/writes something outside `backend/` (i.e., anywhere under the repo root but not under `backend/app/` or `backend/scripts/` themselves, which ARE correctly bind-mounted 1:1) needs the same treatment preemptively: an environment-variable override (`os.environ.get("X_DIR")` falling back to the local relative-path computation) plus a matching bind mount + env var in `infra/docker-compose.yml`. Check for this class of bug specifically whenever adding a script that touches `data/`, `docs/`, or any other repo-root-level directory.

**10. CRITICAL: the user's terminal ("my machine") and this Claude Code sandbox are the SAME environment**
STATUS: Confirmed beyond doubt on 2026-08-22. Evidence: the user's shell prompt is `ubuntu@Ikramusfzi:~/Downloads/HealthCare Project$` — same username (`ubuntu`), same working directory, same git repo/commit history, same missing-then-installed Docker, same file (`PROJECT_CONTEXT.md`) visible to both "sides" in real time. When the user first asked to "run it on my machine to cross-check," Claude assumed a separate personal computer and gave instructions accordingly — wrong assumption, later corrected once the evidence was undeniable (identical hostname/path, `docker: command not found` matching Claude's own earlier finding). IMPACT: High for how Claude should operate going forward. Consequences: (a) files Claude edits are immediately visible in the user's terminal and vice versa — no "pull" step needed between them, though git commits are still real commits either side could make; (b) processes either side starts (dev servers, docker containers) are visible to and can conflict with the other — always check `pgrep`/`docker ps`/port usage before assuming a clean slate; (c) Claude can gain access to privileged resources (like Docker) that the user set up with their own sudo password, via group-membership tricks (`sg docker -c "..."`) without ever needing the password itself; (d) "ask the user to run this on their machine so I can't just do it myself" is NOT a valid framing here — if a tool is installed and group-accessible, Claude should just use it directly instead of relay-testing through the user. NEXT ACTION: At the start of any future session, verify directly (don't assume) whether this is still the setup — check hostname/whoami and try `docker ps`/`sg docker -c "docker ps"` before either assuming Docker is inaccessible or asking the user to test something Claude could just check itself.

**8. `email-validator` (used by Pydantic `EmailStr`) rejects `.test`/`.local`/`.example`/`.invalid` as reserved special-use domains**
STATUS: Confirmed by direct testing. IMPACT: Low, but easy to trip over — any seed/test/dev data using RFC 2606 "safe for docs" domains like `user@example.test` fails Pydantic validation even with `check_deliverability=False`, because the reserved-domain check isn't a deliverability check. `globalcare-demo.com`/`*.globalcare-demo.com` and `demo.globalcare.io` both pass. NEXT ACTION: Keep using `@globalcare-demo.com` for all seed/dev/test email addresses across the codebase (already applied in `seed_dev_users.py`, `seed_synthea.py`, `tests/`).

**9. `pkill -f <pattern>` can match its own invoking shell and kill the whole script mid-run**
STATUS: Confirmed twice this session — a multi-line Bash tool command that both started a background server (e.g. `nohup uvicorn ... --port 8002 &`) and later called `pkill -f "...--port 8002"` sometimes had the pattern also match the wrapping `bash -c '<the whole script text>'` process, killing the script before later lines ran (partial/confusing output, unrelated-looking exit codes like 144). IMPACT: Low but wastes a turn re-diagnosing "why did my script only run halfway." NEXT ACTION: Prefer `kill <specific-pid>` (from `pgrep` run in a separate prior tool call, not inline in the same script) over `pkill -f` with a pattern that might overlap the script's own command text; or use distinct, unlikely-to-collide filter strings.

## 18. Last Working Session

```
DATE: 2026-08-22 (same-day session, continued further still)
WHAT WE DID: Pushed Phase 2 (commit 5206032). User asked to see the work
  running "on my machine" to cross-check it independently. Claude initially
  assumed this meant a separate personal computer and gave generic Docker
  Compose instructions. The user's pasted terminal output revealed this was
  WRONG: their shell prompt (ubuntu@Ikramusfzi:~/Downloads/HealthCare
  Project$) matched this exact sandbox - same user, same path, same repo.
  What they'd actually been looking at was Claude's own leftover uvicorn/vite
  dev servers from an earlier demo in this same session (killed once
  identified). This is now documented prominently as item 10 in section 17 -
  a genuinely important correction to how Claude should operate here.
  Guided the user through installing Docker (sudo apt install docker.io
  docker-compose-v2 - needed the user's own sudo password, which Claude does
  not have and did not ask for) and running docker compose up. This surfaced
  two REAL bugs that no amount of SQLite testing had caught: (1)
  backend/Dockerfile only ever copied app/, never alembic.ini/alembic/
  scripts/ (added in later phases) - migrations and seed scripts failed
  inside the container with "file not found"; also, once that was fixed, the
  Synthea data path (data/synthea/, at the repo root, outside the backend/
  Docker build context) would have resolved wrong inside the container - both
  fixed (Dockerfile COPY additions, SYNTHEA_DATA_DIR env var + bind mount);
  (2) bcrypt was unpinned in requirements.txt, and the fresh Docker build
  resolved a bcrypt version incompatible with passlib==1.7.4 (unmaintained
  since 2020) - broke every password hash/verify call. Claude's own sandbox
  had only avoided this by luck (an old bcrypt was already cached from
  earlier in the session). Fixed by pinning bcrypt==4.0.1 - verified the fix
  directly before telling the user to retry. Also hit and resolved unrelated
  Docker infra hiccups along the way: usermod -aG docker not taking effect in
  an already-open terminal (needs newgrp or a fresh shell), and a transient
  containerd "parent snapshot does not exist" error (resolved by daemon
  restart, not a code issue). Once both real bugs were fixed, the user
  successfully ran the full stack end-to-end: docker compose up -d (all 4
  services healthy), alembic upgrade head against real Postgres, both seed
  scripts, and a real login returning a valid JWT. Claude then independently
  verified this too (not just trusting the user's paste-backs) - discovered
  Claude now has Docker access via `sg docker -c "docker ..."` (the docker
  group exists now that the user created it, no sudo needed for this) and
  directly fetched the live /openapi.json (confirmed all 10 endpoints) and
  queried the real Postgres database directly (confirmed exact expected row
  counts: 200 patients, 50 providers, 50 facilities, 953 health_readings, 52
  users). Updated docs/impmemnentaion-plan.md (all three phase status lines
  now say the Postgres/Docker exit criteria are genuinely met, not
  SQLite-simulated), docs/test-execution-log.md (new "Real Docker Compose +
  PostgreSQL run" section documenting both bugs and the fixes), and this
  file.
WHAT CHANGED: This was the first real end-to-end verification against actual
  infrastructure for the whole project. The "SQLite-verified, Postgres-
  pending" caveat that had applied to every phase status line is now
  resolved. Also: Claude and the user are confirmed to share one live
  environment, which changes how future sessions should approach "ask the
  user to test this" - check it directly first if the tooling is accessible.
WHAT WORKED: Real Docker Compose deployment, real PostgreSQL, real JWT login,
  real data counts matching expectations exactly. Two independent
  verification paths (user's terminal output + Claude's own direct docker/
  psql queries) agreed completely.
WHAT DID NOT WORK initially (both now fixed, see above): Dockerfile missing
  alembic/scripts; unpinned bcrypt incompatible with passlib under a fresh
  Docker build.
CURRENT STATE: Phases 0-2 are now genuinely, independently verified against
  real Docker Compose + PostgreSQL - not a simulation. The Dockerfile/
  bcrypt/docker-compose.yml fixes exist on disk but are NOT YET COMMITTED.
NEXT ACTION: Commit and push the fix files (see section 10's file list);
  then start Phase 3 (Module 2 - Telemedicine Appointment & Consultation)
  per api-spec.md §4.
```

```
DATE: 2026-08-22 (same day, continued yet further)
WHAT WE DID: Committed and pushed the Docker/bcrypt fixes (a503a75). User
  confirmed via a Swagger screenshot that Phase 2's endpoints match
  api-spec.md exactly, then asked to continue per this file's roadmap. Built
  Phase 3 (Module 2 - Telemedicine Appointment & Consultation): schemas
  (appointment.py, consultation.py, +AppointmentReport in report.py), and
  app/api/v1/appointments.py covering POST/GET /appointments, PATCH
  /appointments/{id}/status, POST /consultations, GET
  /consultations/{patientId} - plus GET /providers/{id}/schedule added to
  the existing providers router and GET /reports/appointments added to the
  existing reports router. Business rule: recording a consultation
  auto-transitions the appointment to completed (PRD Module 2 language).
  Role scoping mirrors Phase 2's pattern (doctor sees/acts on only their own
  appointments/schedule; consultation history additionally scoped to the
  doctor's own appointments with that patient). Wrote 10 pytest tests
  (test_appointments.py) - all passed on the first run. Ran ruff+black
  (found and fixed one leftover dead-code block from drafting the
  consultation-history endpoint - a stray if/pass with no effect, cleaned
  up before it became a real bug). Since Docker is now available and the
  backend container bind-mounts app/, restarted the container (no rebuild
  needed) and ran a full live curl walkthrough against real PostgreSQL
  directly - confirmed all 5 new endpoints in /openapi.json, then a
  complete book -> doctor login -> schedule -> status update -> consultation
  (auto-complete verified) -> history -> report -> role-denial sequence, all
  correct, response bodies inspected directly (not just status codes). Hit
  the same terminal-output-truncation artifact from earlier in the session
  when running multi-step curl scripts (see section 17 item 9's pkill note -
  this is a related but distinct rendering quirk, not a real failure) -
  worked around it the same way, by checking the backend container's actual
  request log and re-querying response bodies directly rather than trusting
  the script's own captured stdout.
WHAT CHANGED: Module 2 (Telemedicine) backend is fully built and verified,
  same rigor as Module 1. Two of five PRD modules now have working APIs.
WHAT WORKED: Everything, on the first implementation attempt - no schema
  gaps or bugs found this phase (unlike Phase 2's ADR-018/019 and the
  Docker/bcrypt bugs). Full pytest suite (34 tests) and full live Postgres
  walkthrough both clean.
WHAT DID NOT WORK: Nothing outstanding. The terminal-capture-truncation
  quirk noted above is a display artifact of this tool, not a real problem.
CURRENT STATE: Phase 3 complete and verified, NOT YET COMMITTED.
NEXT ACTION: Commit and push Phase 3 (see section 10's file list); then
  start Phase 4 (Module 3 - Remote Patient Monitoring), which is the first
  phase that actually needs Redis (currently running in Docker Compose but
  unused by the FastAPI app) - vitals ingestion, abnormal-reading detection,
  alert de-duplication, per api-spec.md §5.
```

```
DATE: 2026-08-22 (same day, continued yet further still)
WHAT WE DID: Committed and pushed Phase 3 (f24884a). Built Phase 4 (Module 3
  - Remote Patient Monitoring): app/core/redis_client.py (first real Redis
  usage in the project - a module-level redis.Redis client via get_redis()),
  app/services/vitals.py (pure threshold function, 3 severity tiers across
  all 5 vitals - kept separate from the router specifically so it's unit-
  testable in isolation per Testing-startegy.md's "Unit: business logic"
  category), app/schemas/monitoring.py, and app/api/v1/monitoring.py
  (POST/GET /monitoring/readings, GET /monitoring/alerts, PATCH
  /monitoring/alerts/{id}/acknowledge) - alert de-dup via a 5-minute
  per-patient Redis key, exactly ADR-002's scoped role for Redis. Installed
  the redis pip package (was in requirements.txt since Phase 0 but never
  actually installed in this sandbox until now). Added a FakeRedis class to
  tests/conftest.py (in-memory get/set, no real Redis needed for pytest) and
  wrote 12 new tests (test_vitals.py unit tests + test_monitoring.py router
  tests, including test_abnormal_reading_produces_exactly_one_alert_deduped -
  the literal Phase 4 exit criteria). While building this, tried to actually
  exercise POST /monitoring/readings (Patient-only role) and discovered a
  real blocking gap: patients created via POST /patients have no way to get
  a login at all (PatientCreate only had demographic fields) - so every
  "self (Patient)" access path api-spec.md's role tables promise across
  Modules 1-3 was unreachable via the documented API. Fixed as ADR-020:
  PatientCreate now optionally accepts email/password, mirroring how
  ProviderCreate already works. This is the same pattern as ADR-018 (Phase
  2's assign-patient gap) - found by trying to actually use a promised
  feature, not by reading the spec. Ran ruff+black (clean after two small
  line-length fixes). Restarted the backend container (bind-mounted app/, no
  rebuild) after each round of changes and ran two live E2E scripts against
  real Docker Compose + PostgreSQL + REAL Redis (not the test fake): first
  confirmed all 4 new endpoints in /openapi.json, then a full walkthrough -
  admin creates patient WITH a login (ADR-020) - patient logs in - submits a
  normal reading (no alert) - submits 3 abnormal readings in a row - doctor
  sees EXACTLY ONE alert (severity critical) - reading history shows all 4
  readings - doctor acknowledges the alert. This is the first phase where
  the exit criteria itself (de-dup) was verified against real infrastructure
  rather than just a test double.
WHAT CHANGED: Module 3 (Remote Patient Monitoring) backend fully built and
  verified. Three of five PRD modules now have working, Docker/Postgres/
  Redis-verified APIs. Patients can finally log in at all (ADR-020) - this
  retroactively unblocks "self" access testing for Phases 2-3's endpoints
  too, not just Phase 4's.
WHAT WORKED: Threshold logic, Redis dedup, and role scoping all worked
  correctly on the first pass once ADR-020 was fixed. Full pytest suite (53
  tests) and full live Postgres+Redis walkthrough both clean.
WHAT DID NOT WORK initially (now fixed): patients had no way to obtain a
  login - not a bug introduced this phase, but a pre-existing gap from
  Phase 2 that this phase was the first to actually need and therefore
  the first to notice.
CURRENT STATE: Phase 4 complete and verified against real Redis, NOT YET
  COMMITTED.
NEXT ACTION: Commit and push Phase 4 (see section 10's file list); then
  start Phase 5 (Module 4 - AI-Assisted Health Risk Assessment) - needs
  pandas/numpy/scikit-learn added to requirements.txt (not present yet),
  per api-spec.md §6.
```

```
DATE: 2026-08-22 (same day, continued yet further still)
WHAT WE DID: Committed and pushed Phase 4 (42a587c). Built Phase 5 (Module 4
  - AI-Assisted Health Risk Assessment), the most involved phase so far since
  it needed a genuinely trained ML model, not just CRUD endpoints. Installed
  pandas/numpy/scikit-learn/joblib and pinned them in requirements.txt.
  Designed feature extraction (app/services/risk_features.py - age +5 vitals,
  fixed order) as a module shared verbatim between training and inference
  specifically to avoid train/serve skew. For training labels (no real
  clinical outcomes exist for synthetic patients), deliberately built a
  SEPARATE weighted point-score heuristic (app/services/risk_labels.py)
  rather than reusing Module 3's alert-threshold function - reusing it would
  have made the classifier trivially replicate code that already exists,
  adding no value. First training attempt (one row per patient, latest
  reading only, 200 rows) produced a badly imbalanced dataset (94% low) with
  a near-useless model (macro F1 ~0.49, one class with zero test examples) -
  diagnosed the cause (simulated spo2/temperature rarely contribute risk
  points) and fixed by using every health_reading as an independent training
  row instead (953-957 rows) - meaningfully better (macro F1 ~0.65, low/
  moderate perform well, high still thin at only 3 total examples - real,
  transparently documented in the report, not hidden). Trained a
  RandomForestClassifier, wrote scripts/train_risk_model.py to also generate
  docs/ai-evaluation-report.md (a real exam-brief deliverable, not just
  internal notes) with accuracy/precision/recall/F1/confusion matrix/feature
  importances. Built app/api/v1/ai.py (risk-assessment, predictions history,
  model metadata) with the same doctor-assigned-patient scoping pattern used
  throughout. Wrote 12 new tests (test_risk_features_and_labels.py +
  test_ai.py, run against the actual committed model artifact, not a mock -
  full suite now 65/65). Ran ruff+black (added a per-file E501 ignore for
  the training script's embedded markdown-report f-string, following the
  same reasoning as the alembic/versions/*.py ignore from Phase 2/3). Then
  rebuilt the Docker backend image (first REbuild since Phase 0 - all prior
  phases only needed a container restart since they didn't add new pip
  dependencies) and ran scripts/train_risk_model.py inside the real
  container against real Postgres data (957 readings) - it reported success
  but the evaluation report landed at a container-only /docs/ path, invisible
  on the host. Recognized this immediately as the SAME bug class as Phase 1's
  SYNTHEA_DATA_DIR issue (relative-path navigation that assumes a
  repo-root/backend/scripts/ depth, which doesn't exist inside the container
  where WORKDIR /app IS backend/'s contents directly) - fixed the same way
  (DOCS_DIR env var + ../docs:/docs bind mount), verified the fix locally
  first (default path still correct without the env var), then retrained
  inside the rebuilt container and confirmed via `ls` on the HOST that the
  report actually landed correctly this time. Cross-Python-version check:
  the model was trained under the container's Python 3.11 and successfully
  loaded by pytest running under this sandbox's Python 3.10 - no compat
  issue. Ran a full live curl walkthrough against the real API (model
  metadata, patient submits vitals, doctor runs an assessment, prediction
  history for both doctor and patient-self, role-denial for metadata as a
  doctor) - all correct, response bodies inspected directly (confidence
  0.67, category "low", recommendation text present). Added a new numbered
  item (11) to section 17 documenting this as a RECURRING bug pattern (not
  a one-off) with explicit guidance for future scripts that touch anything
  outside backend/app/ or backend/scripts/.
WHAT CHANGED: Module 4 (AI Risk Assessment) backend fully built, trained,
  and verified. Four of five PRD modules now have working, Docker/Postgres-
  verified APIs - only the Executive Dashboard (Phase 6) remains on the
  backend side, and Phase 6 is also the first phase to need real frontend
  work.
WHAT WORKED: The feature-extraction/label-separation design decision paid
  off immediately - swapping the dataset construction from per-patient to
  per-reading was a clean, well-understood fix once the imbalance was
  diagnosed. The DOCS_DIR bug was caught and fixed on the same turn it
  appeared (a repeat of a known pattern this session had already
  encountered once, so diagnosis was fast).
WHAT DID NOT WORK initially (both now fixed): the first dataset construction
  approach (one row per patient) produced a nearly-useless model; the
  report's Docker output path repeated the Phase 1 SYNTHEA_DATA_DIR bug
  class exactly.
CURRENT STATE: Phase 5 complete and verified against real PostgreSQL
  (including a real training run producing real metrics), NOT YET COMMITTED.
  The trained model artifacts and generated report are real files that need
  to be committed alongside the source code, not just code changes.
NEXT ACTION: Commit and push Phase 5 (see section 10's file list, including
  the generated backend/app/ml_models/ artifacts and docs/ai-evaluation-
  report.md); then start Phase 6 (Module 5 - Executive Healthcare Operations
  Dashboard) - the first phase touching the actual frontend/UI template,
  per api-spec.md §7 and docs/UIUX.md §3.
```

```
DATE: 2026-08-22 (same day, continued yet further still)
WHAT WE DID: Committed and pushed Phase 5 (ac851b0). Built Phase 6 (Module 5
  - Executive Healthcare Operations Dashboard), the first phase to touch the
  frontend since Phase 0's placeholder screen. Backend: app/schemas/
  dashboard.py + app/api/v1/dashboard.py with three shared aggregation
  functions (build_overview, build_trends, build_provider_activity) reused
  by both direct routes and a new GET /reports/executive composing all
  three - real SQL aggregation against patients/appointments/health_
  readings/alerts/predictions, no fabricated figures. Found and fixed a
  string-vs-enum comparison bug (Alert.severity == "critical" doesn't match
  the SQLAlchemy Enum column - fixed to AlertSeverity.CRITICAL). Wrote 7
  pytest tests (test_dashboard.py, suite now 72/72). Frontend: rewrote
  tailwind.config.js with the full "Clinical Precision" design token set
  copied verbatim from the template's embedded Tailwind configs (colors,
  fonts, spacing, border-radius all exact); built an API client, JWT auth
  context, protected routing, a shared TopNav, and three dashboard pages
  (DashboardUnified, DashboardExecutive with a live Chart.js trend line,
  DashboardOperations) faithfully ported from UIUX Design/s5, s2, s17.
  Wherever the template assumed data the platform doesn't track (bed
  occupancy, no-show rate, provider presence/load, a pixel-positioned Gantt
  timeline), substituted a real computable equivalent instead of inventing
  a number - documented as ADR-022 ("honest data only"). Replaced App.jsx's
  Phase 0 placeholder with real routing (Login, 3 dashboard routes, role-
  gated via ProtectedRoute). Verified against the REAL running Docker
  Compose stack (not a second local dev server - localhost:5173 was already
  the live frontend container) via browser automation: logged in as both
  administrator and executive demo users, confirmed all three dashboards
  render correct real data (204 patients, live KPIs, a rendered Chart.js
  canvas), confirmed ProtectedRoute correctly redirects an administrator
  away from /dashboard/executive back to /dashboard, confirmed the
  Executive-only "Export Data" button calls GET /reports/executive (200)
  and triggers a JSON download. Found and fixed three real bugs along the
  way: (1) docker-compose.yml's frontend service only bind-mounted src/ and
  index.html, not tailwind.config.js/postcss.config.js - editing the design
  tokens on the host had no effect until both were added to volumes: and
  the container recreated (docker compose up -d --no-deps frontend) - same
  bug class as SYNTHEA_DATA_DIR/DOCS_DIR (§17 item 11), this time for dev
  tooling; (2) the frontend briefly crashed reading
  overview.appointments_today_by_status.completed because the backend
  container had never been restarted after that field was added to the
  code (uvicorn runs without --reload) - fixed with docker compose restart
  backend, plus defensive optional chaining in the frontend regardless; (3)
  npm run lint reported 30 false-positive errors (fetch/localStorage/
  document/Blob/URL "not defined", every JSX-only component import flagged
  "unused") because eslint.config.js had no browser globals and didn't
  extend eslint-plugin-react's recommended rules - fixed the config (added
  globals.browser + react.configs.recommended.rules) and discovered the
  SAME bind-mount gap applied to eslint.config.js too (fixed as part of bug
  #1's ADR, now ADR-023). Ran the full backend suite on the host Python
  (not the Docker container, which is missing the tests/ bind mount by
  design) - 72 passed, ruff clean, black clean (after reformatting one
  >100-char line in the new dashboard.py).
WHAT CHANGED: All five PRD modules now have working, Docker/Postgres-
  verified backend APIs, AND the Executive Dashboard has a full working
  frontend - the first UI work of the whole project beyond the Phase 0
  placeholder. Mandatory deliverables (Docker Compose deployment, 5
  modules, dashboard) are now functionally complete; what remains is
  observability/security hardening (Phase 7), diagrams/docs polish (Phase
  9), and demo prep (Phase 10) - plus optional AWS (Phase 8).
WHAT WORKED: The shared aggregation-function design (build_overview etc.)
  paid off immediately when GET /reports/executive needed the exact same
  data as the three individual endpoints. The "honest data only" principle
  from earlier phases (real Redis dedup, real trained model) extended
  cleanly to dashboard KPIs without needing new discussion.
WHAT DID NOT WORK initially (all three now fixed): the tailwind/postcss/
  eslint config Docker bind-mount gap; the stale backend container after a
  schema field addition; the ESLint config's missing browser globals and
  JSX-usage detection producing 30 false-positive lint errors.
CURRENT STATE: Phase 6 complete and verified against real Docker Compose +
  PostgreSQL + live browser automation, NOT YET COMMITTED.
NEXT ACTION: Commit and push Phase 6 (see section 10's file list); then
  start Phase 7 (Observability & Security Hardening) - Prometheus metrics,
  Grafana dashboards, OPA policies, Trivy scans, per docs/Security.md.
```

## 19. Claude Instructions

**Before starting work:**
1. Read this file (`PROJECT_CONTEXT.md`) first.
2. `git fetch && git status` against `origin/main` before trusting any local sandbox clone — it may be stale (see §17, item 4).
3. Read only the detailed doc(s) relevant to the current task (§16).
4. Inspect the actual repo tree before assuming anything exists — don't trust this file's §8 blindly if the repo has since changed; re-verify.
5. Do not assume undocumented functionality exists.
6. Do not rewrite documentation unnecessarily — this is a planning-complete project; changes to `docs/` should be deliberate and logged in `docs/deccission.md` if they reflect a real decision.
7. Follow the existing architecture/tech-stack decisions (§13) unless the user explicitly changes one.
8. Keep changes focused on the current task.
9. Update this file after meaningful work (see rules below).
10. This sandbox cannot push to GitHub directly (§17, item 3) — prepare commits, but the user pushes from their own machine unless that constraint has since changed.

**When the user says "continue":**
1. Read `PROJECT_CONTEXT.md`.
2. Identify `CURRENT TASK` (§10).
3. `git fetch`/verify the actual repo state — don't assume it matches this file.
4. Read only the documentation relevant to that task.
5. Review `NEXT IMMEDIATE ACTION` (§11).
6. Continue from the verified current state — don't restart full project analysis.
7. Do not mark anything "Completed" without verifying it against the actual repo/tests.

**Maintenance rule:** Update this file when a feature is completed, major implementation begins, architecture changes, a decision is made, a blocker appears/resolves, the phase changes, or the next major task changes. Do not update for every small edit.
