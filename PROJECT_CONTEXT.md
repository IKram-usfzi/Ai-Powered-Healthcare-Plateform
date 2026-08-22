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
| Telemedicine Appointments | Scheduling, consultations, status tracking | NOT STARTED |
| Remote Patient Monitoring | Vitals ingestion, abnormal-reading alerts | NOT STARTED |
| AI Health Risk Assessment | Lightweight classifier, confidence-scored predictions | NOT STARTED |
| Executive Operations Dashboard | 3-view KPI/ops dashboard (design fully specced) | NOT STARTED (design complete) |

All five are fully specified in `docs/PRD.md`, `docs/api-spec.md`, `docs/backend-schema.md` — none have backend, frontend, or database code written yet.

## 8. Current Implementation Status

**Completed and pushed to GitHub** (`github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform`, `main`):
- Full documentation set (12+ files: PRD, TRD, architecture, api-spec, backend-schema, deccission/ADR log, developement-rules, flow, impmemnentaion-plan, Security, Testing-startegy, UIUX, test-execution-log) and the 25-screen UI/UX template under `UIUX Design/`.
- **Phase 0 — Foundation:** `backend/` (FastAPI skeleton), `frontend/` (React+Vite+Tailwind skeleton), `infra/docker-compose.yml`, root `README.md`, `mkdocs.yml`. Verified: FastAPI health endpoint runs; `mkdocs build --strict` clean; frontend+backend later confirmed running together (see below).
- **Phase 1 — Data & Domain Modeling:** 9 SQLAlchemy models matching `backend-schema.md`, Alembic migration, `fetch_synthea.py`/`seed_synthea.py`. Verified: migration up/down clean on SQLite; seed script loads 200 patients/50 facilities/50 providers/953 health_readings with real Synthea vitals + physiologically-plausible simulated SpO2/temperature.
- **Phase 2 — Module 1 (Patient & Provider Management), this session:** JWT auth (`app/core/security.py`, `app/api/deps.py`) + all `api-spec.md` §2-3 endpoints (`/auth/*`, `/patients`, `/providers`, `/facilities`, `/reports/registration`), with role-based access control including the doctor-scoped "assigned patients only" rule and patient self-access. **Verified two ways:** a full manual curl walkthrough (all happy paths + 3 role-denial checks correct) and 24 automated pytest tests, all passing (`backend/tests/`). Ruff+Black clean. Full details: `docs/test-execution-log.md`.
- Sandbox capability discovery: Node.js and pip can both be obtained without sudo (portable binaries) — see §17 item 7. Frontend was actually run and confirmed talking to the live backend (not just "written but unverified" as earlier sessions had it).
- ADR-016 through ADR-019 (blood pressure split, Synthea-only confirmed, `assigned_provider_id` added to close an api-spec/schema gap, all timestamps made timezone-aware) — each found and fixed during real implementation/verification, not speculative.

**In Progress:** Nothing actively mid-implementation.

**Not Started:**
- Real PostgreSQL/Docker Compose run (still needs a Docker-capable machine — this sandbox has neither Docker nor a way to install Postgres without a sudo password)
- Phases 3-10: telemedicine appointments, remote monitoring, AI risk assessment, executive dashboard, observability/security (OPA/Prometheus/Grafana/Trivy), AWS deployment, the 17 mandatory diagrams as actual files, and any real frontend UI beyond the Phase 0 placeholder screen
- AWS budget alarm status — unknown, unverified

**Blocked:** None currently. Direct git push from this sandbox works once the user supplies a GitHub token (confirmed multiple times this session) — see §17 item 3.

## 9. Current Development Phase

Phases (from `docs/impmemnentaion-plan.md`):
Phase 0 — Foundation · Phase 1 — Data & Domain Modeling · Phase 2 — Module 1 (Patients/Providers) · Phase 3 — Module 2 (Telemedicine) · Phase 4 — Module 3 (Monitoring) · Phase 5 — Module 4 (AI Risk) · Phase 6 — Module 5 (Dashboard) · Phase 7 — Observability/Security · Phase 8 — AWS (stretch) · Phase 9 — Docs/Diagrams · Phase 10 — Testing/Demo Prep

**CURRENT PHASE: Phase 2 — Module 1: Patient & Provider Management (done, pending real-Postgres verification).** All endpoints implemented and tested (manual walkthrough + 24 pytest tests, all passing). Outstanding: a real run against actual PostgreSQL/Docker (this sandbox has neither — see §17 item 7), and pushing this session's commit to GitHub.

## 10. Current Task

```
CURRENT TASK:
Push this session's Phase 2 work, then start Phase 3 (Module 2 — Telemedicine
Appointment & Consultation).

OBJECTIVE:
Scheduling, consultation records, appointment status tracking, provider
schedules, operational reports per api-spec.md §4 and
impmemnentaion-plan.md Phase 3.

STATUS:
Phase 2 committed locally, not yet pushed (need a token or the user's own
push). Phase 3 not yet started.

FILES ADDED/MODIFIED (this session, Phase 2):
backend/app/core/security.py (new, JWT+bcrypt), backend/app/api/deps.py (new,
auth/RBAC dependencies), backend/app/schemas/ (new, Pydantic DTOs),
backend/app/api/v1/{auth,patients,providers,facilities,reports}.py (new),
backend/app/api/v1/router.py, backend/app/main.py (error-shape handler),
backend/app/models/patient.py (+assigned_provider_id, ADR-018), all 9 models
(DateTime(timezone=True) fix, ADR-019), backend/alembic/versions/ (migration
regenerated clean since nothing had been deployed yet), backend/tests/ (new,
24 tests), backend/scripts/seed_dev_users.py (new), backend/pyproject.toml
(ruff/black config additions), docs/deccission.md (+ADR-018/019),
docs/backend-schema.md, docs/impmemnentaion-plan.md (Phase 2 status),
docs/test-execution-log.md (new), docs/README.md, mkdocs.yml, README.md,
infra/README.md.

EXPECTED RESULT:
Commit pushed to github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform main.
```

## 11. NEXT STEPS

1. Commit and push this session's Phase 2 work (needs the user's GitHub token or the user pushing from their own machine — see §17 item 3)
2. Ideally: user runs the real Postgres/Docker path at some point to confirm this sandbox's SQLite-based verification holds
3. Start Phase 3: Module 2 (Telemedicine Appointment & Consultation) — scheduling, consultation records, status tracking, provider schedules, operational reports per `api-spec.md` §4
4. Resolve the still-open decisions listed in §13/§17 before they block later phases

```
NEXT IMMEDIATE ACTION:
Commit the Phase 2 work and push (pending token/user push), then begin
Phase 3: appointments + consultations CRUD per docs/api-spec.md §4.
```

## 12. Project Roadmap

**Phase 0 — Foundation**
- [x] Repository created, pushed to GitHub
- [x] README, ADR log (`deccission.md`)
- [x] `backend/` / `frontend/` / `infra/` folder skeleton (backend and frontend both verified running, together, via a portable Node.js install; `docker-compose.yml` itself still unverified — no Docker in this sandbox)
- [x] `docker-compose.yml` skeleton (written, not yet run — no Docker in this sandbox)
- [x] `.gitignore` strengthened beyond `*.pdf`
- [x] MkDocs initialized (`mkdocs build --strict` verified locally)
- [x] Phase 0 scaffolding committed/pushed to GitHub (commit `367b98b`)
- [ ] AWS budget alarm — status UNKNOWN, needs verification

**Phase 1 — Data & Domain Modeling**
- [x] PostgreSQL schema as real SQLAlchemy models + Alembic migration (verified on SQLite; real Postgres run still pending)
- [x] Synthea dataset pulled/generated and mapped (`fetch_synthea.py`/`seed_synthea.py`, verified: 200 patients/50 facilities/50 providers/953 health_readings)
- [x] Phase 1 work committed/pushed to GitHub (commit `9ba98b2`)

**Phase 2 — Module 1: Patient & Provider Management**
- [x] JWT auth (`/auth/login`, `/auth/refresh`, `/auth/me`)
- [x] Patients/Providers/Facilities CRUD per `api-spec.md` §3
- [x] Role model + doctor-scoped/patient-self-access authorization
- [x] Registration report (`/reports/registration`)
- [x] 24 automated pytest tests, all passing; manual E2E curl walkthrough verified
- [ ] This session's Phase 2 work committed/pushed to GitHub — pending token/user push

**Phase 3–6 — Modules 2–5 (backend + frontend + AI)**
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
STATUS: Confirmed and refined this session. `apt-cache policy postgresql` shows it's installable but not installed; `sudo -ln` requires a password we don't have — did not attempt to bypass this (PostgreSQL genuinely cannot be run here). BUT: pip was obtained via `curl bootstrap.pypa.io/get-pip.py | python3 - --user` (no sudo needed), and Node v20.18.1 was obtained by downloading the official portable tarball (`nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.xz`, ~26 MB) and extracting to `~/.local/node` (no sudo needed) — both installed outside the project directory, in the sandbox user's home dir, so they may or may not persist into a future session depending on sandbox lifecycle; re-check with `node --version`/`pip3 --version` rather than assuming either is gone or present. IMPACT: Low now for backend+frontend verification — both actually ran together this session (`npm install` succeeded, `npm run dev` served the real Vite/React/Tailwind app, which successfully fetched `/api/v1/health` from the live FastAPI backend, confirming CORS and the full non-Docker stack wiring). Remaining gap is narrower: only Docker itself and real PostgreSQL are unverifiable here (Docker needs cgroups/namespaces typically requiring root in a container sandbox — not attempted; real Postgres needs either Docker or a sudo-gated apt install). NEXT ACTION: If Node/pip aren't already present at the start of a session, re-fetch them the same way before assuming frontend work can't be verified. Still don't claim `docker compose up` or a real PostgreSQL run works without the user (or a Docker-capable environment) actually confirming it — that gap is real and unchanged.

**8. `email-validator` (used by Pydantic `EmailStr`) rejects `.test`/`.local`/`.example`/`.invalid` as reserved special-use domains**
STATUS: Confirmed by direct testing. IMPACT: Low, but easy to trip over — any seed/test/dev data using RFC 2606 "safe for docs" domains like `user@example.test` fails Pydantic validation even with `check_deliverability=False`, because the reserved-domain check isn't a deliverability check. `globalcare-demo.com`/`*.globalcare-demo.com` and `demo.globalcare.io` both pass. NEXT ACTION: Keep using `@globalcare-demo.com` for all seed/dev/test email addresses across the codebase (already applied in `seed_dev_users.py`, `seed_synthea.py`, `tests/`).

**9. `pkill -f <pattern>` can match its own invoking shell and kill the whole script mid-run**
STATUS: Confirmed twice this session — a multi-line Bash tool command that both started a background server (e.g. `nohup uvicorn ... --port 8002 &`) and later called `pkill -f "...--port 8002"` sometimes had the pattern also match the wrapping `bash -c '<the whole script text>'` process, killing the script before later lines ran (partial/confusing output, unrelated-looking exit codes like 144). IMPACT: Low but wastes a turn re-diagnosing "why did my script only run halfway." NEXT ACTION: Prefer `kill <specific-pid>` (from `pgrep` run in a separate prior tool call, not inline in the same script) over `pkill -f` with a pattern that might overlap the script's own command text; or use distinct, unlikely-to-collide filter strings.

## 18. Last Working Session

```
DATE: 2026-08-22 (same-day session, continued further)
WHAT WE DID: Pushed Phase 1 (commit 9ba98b2). User asked to "see the working
  stuff" — got a portable Node.js v20 running (no sudo, tarball from
  nodejs.org), ran npm install + npm run dev for real, and showed both the
  live backend (Swagger /docs) and live frontend (fetching the backend's
  health check) in the Browser pane. This upgraded frontend verification from
  "written but untested" to "actually confirmed running." Then built Phase 2
  (Module 1 API): JWT auth (app/core/security.py: bcrypt + jose), RBAC
  dependencies (app/api/deps.py: require_roles factory, interim substitute
  for the OPA policies planned in Phase 7), Pydantic schemas, and all
  api-spec.md §2-3 endpoints (auth, patients, providers, facilities,
  registration report) with the doctor-scoped/patient-self-access rules from
  Security.md §3. Found and fixed two real schema gaps while implementing:
  ADR-018 (patients.assigned_provider_id didn't exist — the assign-patient
  endpoint had nothing to write to) and ADR-019 (every timestamp column was
  timezone-naive while every default value was timezone-aware — a latent
  PostgreSQL bug). Since no migration had been deployed anywhere yet, the two
  existing migrations were deleted and regenerated as one clean "initial
  schema" migration rather than layering a third fix-up migration on top.
  Wrote 24 pytest tests (backend/tests/) covering happy paths, 404s, role
  denial, patient self-access, and duplicate-email conflicts — all passing.
  Also ran a full manual curl walkthrough against a live server first, which
  caught two real things: (1) email-validator rejects .test/.local as
  reserved domains (switched all seed/test emails to @globalcare-demo.com),
  (2) a stale SQLite file descriptor from an earlier manual test produced a
  transient "readonly database" error (sandbox artifact, not an app bug —
  resolved by fully killing old server processes and using a fresh DB
  filename). Ran ruff+black, fixed all findings (reverted a Python-3.11-only
  UP017 auto-fix since this sandbox only has 3.10; configured
  extend-immutable-calls for FastAPI's Depends()-as-default pattern; per-file
  F821 ignore for SQLAlchemy's Mapped["ClassName"] forward refs). Created
  docs/test-execution-log.md (Testing-startegy.md §7's "test execution
  summary" deliverable) and caught/fixed a real mkdocs --strict failure from
  a prior session's edit (docs/README.md had markdown links pointing outside
  docs_dir).
WHAT CHANGED: Repo now has a real, tested REST API for Module 1, not just a
  data layer. Committed locally, not yet pushed this half of the session.
WHAT WORKED: Everything, verified two independent ways (manual + automated).
  24/24 pytest tests pass. ruff and black both clean. mkdocs --strict clean.
  Migration up/down/up cycle clean on SQLite.
WHAT DID NOT WORK / COULD NOT BE VERIFIED: Still no real PostgreSQL/Docker
  run — same gap as Phase 0/1, unchanged. Don't claim it's verified without
  the user (or a Docker-capable environment) actually confirming it.
CURRENT STATE: Phase 2 functionally complete pending (a) a real Postgres/
  Docker run and (b) pushing this session's commit to GitHub.
NEXT ACTION: Commit this session's Phase 2 work; ask the user how they want
  to push; then start Phase 3 (Module 2 — Telemedicine Appointment &
  Consultation) per api-spec.md §4.
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
