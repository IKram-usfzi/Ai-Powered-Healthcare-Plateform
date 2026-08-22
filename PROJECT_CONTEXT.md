# Project Context

> Read this file first, every session. It is project memory, not documentation — for depth, follow the file paths under each section into `docs/`.

## 1. Project Identity

- **Project name:** GlobalCare — Enterprise Remote Healthcare Management Platform (GitHub repo: `Ai-Powered-Healthcare-Plateform`)
- **Project type:** Academic capstone (Diploma in AIOPS, EduQual Level 6, al-Nafi International College) — built as a real proof-of-concept enterprise web platform, not a toy exercise
- **Project purpose:** Design, document, and build a proof-of-concept healthcare platform for a fictional client, "GlobalCare Telehealth Network," to pass a 3-stage exam (presentation, live demo + GitHub review, viva voce)
- **Current development stage:** Phases 0-2 done and verified locally. Database schema (9 SQLAlchemy models + Alembic migration), Synthea seed data, and a working JWT-authenticated REST API for Module 1 (patients/providers/facilities/registration reporting) all exist and are tested (24 passing pytest tests + a manual end-to-end curl walkthrough). Frontend is still just the Phase 0 placeholder screen — no real UI for any module yet (Phase 6).
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
| Patient & Provider Management | Registration, profiles, facility/provider assignment | BACKEND API DONE (Phase 2) — frontend UI not started (Phase 6) |
| Telemedicine Appointments | Scheduling, consultations, status tracking | BACKEND API DONE (Phase 3) — frontend UI not started (Phase 6) |
| Remote Patient Monitoring | Vitals ingestion, abnormal-reading alerts | NOT STARTED |
| AI Health Risk Assessment | Lightweight classifier, confidence-scored predictions | NOT STARTED |
| Executive Operations Dashboard | 3-view KPI/ops dashboard (design fully specced) | NOT STARTED (design complete) |

All five are fully specified in `docs/PRD.md`, `docs/api-spec.md`, `docs/backend-schema.md` — none have backend, frontend, or database code written yet.

## 8. Current Implementation Status

**Completed and pushed to GitHub** (`github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform`, `main`):
- Full documentation set (12+ files: PRD, TRD, architecture, api-spec, backend-schema, deccission/ADR log, developement-rules, flow, impmemnentaion-plan, Security, Testing-startegy, UIUX, test-execution-log) and the 25-screen UI/UX template under `UIUX Design/`.
- **Phase 0 — Foundation:** `backend/` (FastAPI skeleton), `frontend/` (React+Vite+Tailwind skeleton), `infra/docker-compose.yml`, root `README.md`, `mkdocs.yml`. Verified: FastAPI health endpoint runs; `mkdocs build --strict` clean; frontend+backend later confirmed running together (see below).
- **Phase 1 — Data & Domain Modeling:** 9 SQLAlchemy models matching `backend-schema.md`, Alembic migration, `fetch_synthea.py`/`seed_synthea.py`. Verified: migration up/down clean on SQLite; seed script loads 200 patients/50 facilities/50 providers/953 health_readings with real Synthea vitals + physiologically-plausible simulated SpO2/temperature.
- **Phase 2 — Module 1 (Patient & Provider Management):** JWT auth (`app/core/security.py`, `app/api/deps.py`) + all `api-spec.md` §2-3 endpoints (`/auth/*`, `/patients`, `/providers`, `/facilities`, `/reports/registration`), with role-based access control including the doctor-scoped "assigned patients only" rule and patient self-access. Ruff+Black clean.
- **Real Docker Compose + PostgreSQL verification (2026-08-22)** — see §17 item 7 for the critical context (the user's "own machine" turned out to be this same sandbox). `docker compose up -d` (postgres+redis+backend+frontend) all healthy; `alembic upgrade head` applied against real Postgres; `seed_dev_users.py` + `seed_synthea.py` loaded real data; a real login returned a valid JWT. **Independently confirmed by Claude directly** (not just relying on the user's paste-backs) via `sg docker -c "docker ..."`: fetched the live `/openapi.json` (all 10 endpoints present) and queried the real Postgres database directly (200 patients, 50 providers, 50 facilities, 953 health_readings, 52 users — exact expected counts). This closes the "SQLite-verified, Postgres-pending" caveat that had applied to every phase. Two real bugs were caught and fixed by this real-infra run — see next bullet.
- ADR-016 through ADR-019 (blood pressure split, Synthea-only confirmed, `assigned_provider_id` added to close an api-spec/schema gap, all timestamps made timezone-aware) — found during implementation/verification. Two more real bugs found by the *Docker* run specifically (not caught by SQLite testing): (a) `backend/Dockerfile` never learned to copy `alembic.ini`/`alembic/`/`scripts/` when those were added in Phase 1-2 — fixed, plus a related fix so the Synthea data path resolves correctly via a `SYNTHEA_DATA_DIR` env var + bind mount; (b) `bcrypt` was unpinned in `requirements.txt` and pip resolved a version incompatible with `passlib==1.7.4` inside the fresh Docker build (worked in the authoring sandbox only by luck, on an old cached bcrypt) — fixed by pinning `bcrypt==4.0.1`. Full details: `docs/test-execution-log.md`.
- **Phase 3 — Module 2 (Telemedicine Appointment & Consultation):** all `api-spec.md` §4 endpoints (`/appointments` POST/GET, `/appointments/{id}/status` PATCH, `/consultations` POST, `/consultations/{patientId}` GET, `/providers/{id}/schedule` GET, `/reports/appointments` GET). Recording a consultation auto-completes its appointment. Verified two ways: 10 new pytest tests (suite now 34/34 passing) and a live Docker Compose + PostgreSQL walkthrough (restarted the backend container to pick up the bind-mounted code, no rebuild needed) — book → doctor login → view schedule → update status → record consultation → history → report → role-denial check, all correct, response bodies inspected directly. No new bugs found this time — everything worked on the first try. Full details: `docs/test-execution-log.md`.

**In Progress:** Nothing actively mid-implementation.

**Not Started:**
- Phases 4-10: remote monitoring, AI risk assessment, executive dashboard, observability/security (OPA/Prometheus/Grafana/Trivy), AWS deployment, the 17 mandatory diagrams as actual files, and any real frontend UI beyond the Phase 0 placeholder screen
- AWS budget alarm status — unknown, unverified

**Blocked:** None currently. Direct git push from this sandbox works once the user supplies a GitHub token (confirmed multiple times this session) — see §17 item 3.

## 9. Current Development Phase

Phases (from `docs/impmemnentaion-plan.md`):
Phase 0 — Foundation · Phase 1 — Data & Domain Modeling · Phase 2 — Module 1 (Patients/Providers) · Phase 3 — Module 2 (Telemedicine) · Phase 4 — Module 3 (Monitoring) · Phase 5 — Module 4 (AI Risk) · Phase 6 — Module 5 (Dashboard) · Phase 7 — Observability/Security · Phase 8 — AWS (stretch) · Phase 9 — Docs/Diagrams · Phase 10 — Testing/Demo Prep

**CURRENT PHASE: Phase 3 — Module 2: Telemedicine Appointment & Consultation (DONE, fully verified against real Docker Compose + PostgreSQL).** All endpoints implemented and tested two ways: 10 new pytest tests (suite now 34/34) and a live Docker Compose + PostgreSQL walkthrough verified directly by Claude. No new bugs found this round.

## 10. Current Task

```
CURRENT TASK:
Commit and push Phase 3, then start Phase 4 (Module 3 — Remote Patient
Monitoring).

OBJECTIVE:
Vitals ingestion endpoints, abnormal-reading detection rules, clinical
alerting, Redis wired in for de-duplication, per api-spec.md §5 and
impmemnentaion-plan.md Phase 4. Redis is not wired into the FastAPI app at
all yet (docker-compose.yml runs the redis container, but nothing in
backend/app/ connects to it) - this is the first phase that actually needs it.

STATUS:
Phase 2 (5206032) and the Docker/bcrypt fixes (a503a75) are pushed. Phase 3
work is complete and verified but NOT YET COMMITTED as of this note.

FILES TO COMMIT NEXT (Phase 3):
backend/app/schemas/appointment.py, consultation.py, report.py (+AppointmentReport),
backend/app/api/v1/appointments.py (new), providers.py (+schedule endpoint),
reports.py (+appointments endpoint), router.py, backend/tests/test_appointments.py
(new, 10 tests), docs/impmemnentaion-plan.md (Phase 3 status),
docs/test-execution-log.md (+Phase 3 section), PROJECT_CONTEXT.md (this file).

EXPECTED RESULT:
Commit pushed to github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform main.
```

## 11. NEXT STEPS

1. Commit and push Phase 3 (needs the user's GitHub token or the user pushing themselves — see §17 item 3)
2. Start Phase 4: Module 3 (Remote Patient Monitoring) — vitals ingestion, abnormal-reading detection, alerting, first real use of Redis, per `api-spec.md` §5
3. Resolve the still-open decisions listed in §13/§17 before they block later phases

```
NEXT IMMEDIATE ACTION:
Commit Phase 3 and push (pending token/user push), then begin Phase 4:
monitoring readings + alerts + Redis de-dup per docs/api-spec.md §5.
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
- [ ] Phase 3 work committed/pushed to GitHub — pending token/user push

**Phase 4–6 — Modules 3–5 (backend + frontend + AI)**
- [ ] Not started (any module)

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
- **Dashboard = 3 cooperating views** (Unified/Executive/Operations), not one screen — see `docs/UIUX.md` §3

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
STATUS: Partially resolved. (a) Synthea-only vs. + supplementary Kaggle vitals dataset (ADR-011) — RESOLVED this session as ADR-017 (Synthea only). Still open: (b) dashboard routing — 3 routes vs. role-based default (`docs/UIUX.md` §5), (c) whether `UIUX Design/s22` (Documents) and `s25` (Patient Mobile App) are in scope at all — neither is a mandatory module, (d) AWS account creation date (pre/post 15 Jul 2025) — determines which AWS Free Tier model applies, unknown/unverified. NEXT ACTION: Resolve before the phase that needs each decision (Phase 6 for (b)/(c), Phase 8 for (d)).

**6. AWS budget alarm status**
STATUS: UNKNOWN — needs verification. Phase 0's exit criteria calls for one; not confirmed done or not done. NEXT ACTION: Verify before any AWS work (Phase 8) begins.

**7. This sandbox has no Docker, no PostgreSQL, and no passwordless sudo. Node/npm and pip are NOT pre-installed but CAN be obtained without sudo (portable binaries) — do this at the start of any session that needs them, don't assume they're still there from a prior session.**
STATUS: MOSTLY OBSOLETE as of 2026-08-22 — see the critical correction in item 10 below (**the user's terminal and this sandbox are the same machine**). Docker is now installed here (the user ran `sudo apt install docker.io docker-compose-v2`) and PostgreSQL runs fine as a container. Node/pip were already confirmed obtainable without sudo (portable binaries) earlier in the session — that part still stands. What remains true: no *passwordless* sudo (the user has the password and types it interactively; Claude does not and should not try to obtain it). IMPACT: None now for Docker/Postgres verification — both are fully available. NEXT ACTION: At the start of a future session, check `docker ps` / `sg docker -c "docker ps"` before assuming Docker is unavailable — it may already be installed from this session. If a fresh sandbox genuinely has none of this (Docker, Node, pip), the original acquisition steps in this item's history still apply: get-pip.py --user for pip, the nodejs.org portable tarball for Node, `sudo apt install docker.io docker-compose-v2` for Docker (ask the user to run the sudo-gated step themselves, or if Claude and the user share a terminal, ask the user to run it and then Claude can access it via `sg docker -c "..."` once the docker group exists — no sudo needed for that part).

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
