# Project Context

> Read this file first, every session. It is project memory, not documentation — for depth, follow the file paths under each section into `docs/`.

## 1. Project Identity

- **Project name:** GlobalCare — Enterprise Remote Healthcare Management Platform (GitHub repo: `Ai-Powered-Healthcare-Plateform`)
- **Project type:** Academic capstone (Diploma in AIOPS, EduQual Level 6, al-Nafi International College) — built as a real proof-of-concept enterprise web platform, not a toy exercise
- **Project purpose:** Design, document, and build a proof-of-concept healthcare platform for a fictional client, "GlobalCare Telehealth Network," to pass a 3-stage exam (presentation, live demo + GitHub review, viva voce)
- **Current development stage:** Phase 0 (Foundation) and Phase 1 (Data & Domain Modeling) done and verified locally. All 9 database entities exist as SQLAlchemy models with a working Alembic migration, and a Synthea-derived sample dataset loads successfully. No REST API business logic yet (Phase 2+) — only a health-check endpoint and a placeholder React screen.
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
| Patient & Provider Management | Registration, profiles, facility/provider assignment | NOT STARTED |
| Telemedicine Appointments | Scheduling, consultations, status tracking | NOT STARTED |
| Remote Patient Monitoring | Vitals ingestion, abnormal-reading alerts | NOT STARTED |
| AI Health Risk Assessment | Lightweight classifier, confidence-scored predictions | NOT STARTED |
| Executive Operations Dashboard | 3-view KPI/ops dashboard (design fully specced) | NOT STARTED (design complete) |

All five are fully specified in `docs/PRD.md`, `docs/api-spec.md`, `docs/backend-schema.md` — none have backend, frontend, or database code written yet.

## 8. Current Implementation Status

**Completed** (verified locally in this sandbox; not yet pushed — see §17 item 3):
- Full documentation set (12 files) committed and pushed: PRD, TRD, architecture, api-spec, backend-schema, deccission (ADR log), developement-rules, flow, impmemnentaion-plan, Security, Testing-startegy, UIUX
- UI/UX template received and catalogued — 25 screens, "Clinical Precision" design system, pushed to the repo under `UIUX Design/`
- GitHub repository created and pushed by the user directly from their own machine: `github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform`, branch `main`, commit `efe49df` ("Initial commit: project docs, UI/UX designs, and technology stack")
- Tech stack, architecture, database schema (design-level, no DDL yet), API contract (design-level, no code yet), and 15 ADRs decided and documented (ADR-013/014/015 added this session for ORM/lint/frontend-build tooling)
- **Phase 0 (Foundation) scaffolding, built and verified this session:**
  - `backend/` — FastAPI app (`app/main.py`, `app/core/config.py`, `app/api/v1/health.py` + router), `requirements.txt` (pinned), `pyproject.toml` (Black+Ruff config), `Dockerfile`, `.env.example`. **Verified: ran `uvicorn app.main:app` directly in the sandbox (Docker unavailable here) — `GET /api/v1/health` returned `{"status":"ok"}`, `/docs` returned 200.**
  - `frontend/` — React + Vite + Tailwind app (`src/App.jsx` pings the backend health endpoint), `package.json`, `vite.config.js`, `tailwind.config.js`, `postcss.config.js`, `eslint.config.js`, `Dockerfile`, `.env.example`. **Not executed** — no Node/npm in this sandbox; config was written carefully but only visually reviewed, not run.
  - `infra/docker-compose.yml` — wires `postgres`, `redis`, `backend`, `frontend` with healthchecks; `infra/README.md` documents quick start. **Not executed** — no Docker in this sandbox; deliberately avoids requiring a pre-existing `.env` file so it should run out of the box, but this is unverified.
  - Root `README.md` created (previously missing — was §17 known issue #2, now resolved).
  - `.gitignore` strengthened: added Python/Node/env/OS ignores (previously only `*.pdf` — was §17 known issue #1, now resolved).
  - `mkdocs.yml` + `docs-requirements.txt` (mkdocs-material). **Verified: `mkdocs build --strict` succeeded with zero warnings.**
  - Doc cross-references updated to reflect these decisions: `docs/deccission.md` (ADR-013/014/015), `docs/developement-rules.md` §3, `docs/backend-schema.md` §5, `docs/TRD.md` §5, `docs/README.md` status line, `docs/impmemnentaion-plan.md` Phase 0 status.

**In Progress:**
- Nothing actively mid-implementation. Phase 0 scaffolding is functionally complete pending a real `docker compose up` run on the student's own machine (this sandbox has no Docker/Node — see §17 item 7).

**Phase 1 (Data & Domain Modeling), built and verified this session:**
- `backend/app/models/` — 9 SQLAlchemy 2.0 models (User, Patient, Provider, Facility, Appointment,
  Consultation, HealthReading, Alert, Prediction) matching `docs/backend-schema.md` exactly, plus
  `app/models/enums.py` (UserRole, AppointmentStatus, AlertSeverity, AlertStatus, RiskCategory) and
  `app/db/base.py` (engine/session/Base). **Verified:** `configure_mappers()` succeeds, no relationship errors.
- `backend/alembic/` — initial migration (`788de84b0f84_initial_schema.py`) autogenerated from the
  models. **Verified:** `alembic upgrade head` and `alembic downgrade base` both succeed against
  SQLite (no PostgreSQL in this sandbox — real Postgres run still pending, see §17 item 7).
- `backend/scripts/fetch_synthea.py` + `seed_synthea.py` — downloads the Synthea CSV sample
  (`synthetichealth.github.io/synthea-sample-data`, 8.98 MB zip — note: `synthea.mitre.org`
  directly failed TLS verification from this sandbox, used the GitHub-hosted mirror instead) and
  maps it into the schema. **Verified end-to-end:** 200 sampled patients → 50 facilities, 50
  providers, 953 `health_readings` rows; heart_rate/systolic_bp/diastolic_bp/glucose are real
  Synthea LOINC-coded observation values, spo2/temperature are simulated (real data only covers
  ~5% of encounters for those two). Fixed a real bug found during verification: provider name
  cleaning left embedded digits (e.g. "Tomas436 Sauer") because Synthea's provider `NAME` field
  isn't pre-split like patients' FIRST/LAST — now strips trailing digits per word, not just at the
  string's end.
- ADR-016 (blood pressure split into `systolic_bp`/`diastolic_bp`) and ADR-017 (ADR-011 resolved:
  Synthea only, no supplementary Kaggle dataset — confirmed by directly inspecting the downloaded
  CSV's LOINC codes before deciding) added to `docs/deccission.md`; `docs/backend-schema.md` §6
  (new) documents the Synthea → schema field mapping.

**Not Started:**
- MkDocs site not yet published (build verified locally, not deployed)
- Any of the 17 mandatory architecture diagrams as actual diagram files (only described in prose in `docs/architecture.md` and `docs/flow.md`; the ERD in `backend-schema.md` §1 is Mermaid source, not yet exported)
- AWS deployment (stretch goal) — not started
- All real API business logic for Modules 1–5 (auth, patients, appointments, monitoring, AI, dashboard endpoints) — only a health-check endpoint exists so far; Phase 2 starts this

**Blocked:**
- None currently. (Direct git push *from this cloud sandbox* was blocked in an earlier session by the sandbox's own git proxy when no token was supplied; this session pushed successfully once the user supplied a PAT directly. See §17 item 3 — treat as "works when a token is provided," not "always blocked.")

## 9. Current Development Phase

Phases (from `docs/impmemnentaion-plan.md`):
Phase 0 — Foundation · Phase 1 — Data & Domain Modeling · Phase 2 — Module 1 (Patients/Providers) · Phase 3 — Module 2 (Telemedicine) · Phase 4 — Module 3 (Monitoring) · Phase 5 — Module 4 (AI Risk) · Phase 6 — Module 5 (Dashboard) · Phase 7 — Observability/Security · Phase 8 — AWS (stretch) · Phase 9 — Docs/Diagrams · Phase 10 — Testing/Demo Prep

**CURRENT PHASE: Phase 1 — Data & Domain Modeling (functionally complete, pending real-Postgres verification).** Done: 9 SQLAlchemy models, Alembic migration (verified on SQLite), Synthea CSV obtained and mapped, ADR-011 resolved as ADR-017, `backend-schema.md` finalized (ADR-016). Outstanding: a real `alembic upgrade head` run against actual PostgreSQL (needs Docker — not available in this sandbox, and no sudo to install Postgres locally either — see §17 item 7), and pushing this session's commits to GitHub.

## 10. Current Task

```
CURRENT TASK:
Get this session's Phase 1 work pushed to GitHub, then start Phase 2
(Module 1 — Patient & Provider Management API).

OBJECTIVE:
Build real REST endpoints per api-spec.md §3 (POST/GET /patients, /providers,
/facilities, assign-patient, registration report), with JWT auth foundation
and the role model (Patient/Doctor/Admin/Executive), per
impmemnentaion-plan.md Phase 2.

STATUS:
Phase 1 committed locally, not yet pushed (need a token or the user's own
push). Phase 2 not yet started.

FILES BEING MODIFIED (this session, Phase 1):
backend/app/db/ (new), backend/app/models/ (new, 9 entities + enums),
backend/alembic/ (new, initial migration), backend/scripts/fetch_synthea.py,
backend/scripts/seed_synthea.py (new), .gitignore (+data/synthea/raw/, *.db),
docs/deccission.md (+ADR-016/017), docs/backend-schema.md (§2 BP split, new §6),
docs/impmemnentaion-plan.md (Phase 1 status), infra/README.md (DB setup steps).

EXPECTED RESULT:
Commit pushed to github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform main.
User (or a Docker-capable environment) then runs the real
`docker compose up` → `alembic upgrade head` → `seed_synthea.py` sequence
against actual PostgreSQL to get the verification this sandbox can't provide.
```

## 11. NEXT STEPS

1. Commit and push this session's Phase 1 work (needs the user's GitHub token or the user pushing from their own machine — see §17 item 3)
2. Ideally: user runs the real Postgres path (`docker compose up` → `alembic upgrade head` → seed script) at some point to confirm this sandbox's SQLite-based verification actually holds on Postgres too
3. Start Phase 2: Module 1 (Patient & Provider Management) — CRUD endpoints per `api-spec.md` §3, JWT auth foundation, role model, registration report
4. Resolve the still-open decisions listed in §13/§17 before they block later phases

```
NEXT IMMEDIATE ACTION:
Commit the Phase 1 work and push (pending token/user push), then begin
Phase 2: JWT auth foundation + Module 1 CRUD endpoints
(patients/providers/facilities) per docs/api-spec.md §2-3.
```

## 12. Project Roadmap

**Phase 0 — Foundation**
- [x] Repository created, pushed to GitHub
- [x] README, ADR log (`deccission.md`)
- [x] `backend/` / `frontend/` / `infra/` folder skeleton (written; backend verified running, frontend/infra not — no Node/Docker in this sandbox)
- [x] `docker-compose.yml` skeleton (written, not yet run — no Docker in this sandbox)
- [x] `.gitignore` strengthened beyond `*.pdf`
- [x] MkDocs initialized (`mkdocs build --strict` verified locally)
- [x] Phase 0 scaffolding committed/pushed to GitHub (commit `367b98b`)
- [ ] AWS budget alarm — status UNKNOWN, needs verification

**Phase 1 — Data & Domain Modeling**
- [x] PostgreSQL schema as real SQLAlchemy models + Alembic migration (verified on SQLite; real Postgres run still pending)
- [x] Synthea dataset pulled/generated and mapped (`fetch_synthea.py`/`seed_synthea.py`, verified: 200 patients/50 facilities/50 providers/953 health_readings)
- [ ] This session's Phase 1 work committed/pushed to GitHub — pending token/user push

**Phase 2–6 — Modules 1–5 (backend + frontend + AI)**
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

**3. Direct git push from a cloud/Claude-Code sandbox is blocked**
STATUS: Confirmed — this session's sandbox git proxy rejected pushes to this repo ("not in this session's authorized repository set"). IMPACT: Medium for workflow — any future cloud-sandbox session cannot push directly; the user must push from their own machine (as they successfully did for the current commit). NEXT ACTION: None required unless the user wants to fix the sandbox authorization; otherwise just remember this constraint.

**4. Cloud sandbox local clones go stale**
STATUS: Confirmed — an earlier local clone in a prior session diverged from what the user actually pushed (different file set/commit). IMPACT: Medium — future sessions must `git fetch && git reset --hard origin/main` (after checking for uncommitted work) before trusting the local tree, never assume the local sandbox clone is current. NEXT ACTION: Standard practice for every new session (see §19).

**5. Several design decisions still open**
STATUS: Partially resolved. (a) Synthea-only vs. + supplementary Kaggle vitals dataset (ADR-011) — RESOLVED this session as ADR-017 (Synthea only). Still open: (b) dashboard routing — 3 routes vs. role-based default (`docs/UIUX.md` §5), (c) whether `UIUX Design/s22` (Documents) and `s25` (Patient Mobile App) are in scope at all — neither is a mandatory module, (d) AWS account creation date (pre/post 15 Jul 2025) — determines which AWS Free Tier model applies, unknown/unverified. NEXT ACTION: Resolve before the phase that needs each decision (Phase 6 for (b)/(c), Phase 8 for (d)).

**6. AWS budget alarm status**
STATUS: UNKNOWN — needs verification. Phase 0's exit criteria calls for one; not confirmed done or not done. NEXT ACTION: Verify before any AWS work (Phase 8) begins.

**7. This sandbox has no Docker, no PostgreSQL, and no passwordless sudo. Node/npm and pip are NOT pre-installed but CAN be obtained without sudo (portable binaries) — do this at the start of any session that needs them, don't assume they're still there from a prior session.**
STATUS: Confirmed and refined this session. `apt-cache policy postgresql` shows it's installable but not installed; `sudo -ln` requires a password we don't have — did not attempt to bypass this (PostgreSQL genuinely cannot be run here). BUT: pip was obtained via `curl bootstrap.pypa.io/get-pip.py | python3 - --user` (no sudo needed), and Node v20.18.1 was obtained by downloading the official portable tarball (`nodejs.org/dist/v20.18.1/node-v20.18.1-linux-x64.tar.xz`, ~26 MB) and extracting to `~/.local/node` (no sudo needed) — both installed outside the project directory, in the sandbox user's home dir, so they may or may not persist into a future session depending on sandbox lifecycle; re-check with `node --version`/`pip3 --version` rather than assuming either is gone or present. IMPACT: Low now for backend+frontend verification — both actually ran together this session (`npm install` succeeded, `npm run dev` served the real Vite/React/Tailwind app, which successfully fetched `/api/v1/health` from the live FastAPI backend, confirming CORS and the full non-Docker stack wiring). Remaining gap is narrower: only Docker itself and real PostgreSQL are unverifiable here (Docker needs cgroups/namespaces typically requiring root in a container sandbox — not attempted; real Postgres needs either Docker or a sudo-gated apt install). NEXT ACTION: If Node/pip aren't already present at the start of a session, re-fetch them the same way before assuming frontend work can't be verified. Still don't claim `docker compose up` or a real PostgreSQL run works without the user (or a Docker-capable environment) actually confirming it — that gap is real and unchanged.

## 18. Last Working Session

```
DATE: 2026-08-22 (same-day session, continued)
WHAT WE DID: Pushed the Phase 0 commit (367b98b) once the user supplied a
  GitHub token — pushed without -u this time so the token was never written
  to .git/config (a slip from the previous push, caught and avoided). Then
  built Phase 1 (Data & Domain Modeling): 9 SQLAlchemy 2.0 models under
  backend/app/models/ matching backend-schema.md, app/db/base.py, and an
  Alembic setup (backend/alembic/) with an autogenerated initial migration.
  Installed sqlalchemy/alembic/psycopg[binary] via pip --user. Verified the
  migration applies and reverses cleanly against SQLite (no Postgres in this
  sandbox, and no passwordless sudo to install it — confirmed via `sudo -ln`,
  did not attempt to bypass). Searched for and downloaded the Synthea CSV
  sample dataset (synthea.mitre.org itself failed TLS verification from this
  sandbox; used the synthetichealth.github.io/synthea-sample-data GitHub
  Pages mirror instead, resolved via its GitHub API-backed downloads listing).
  Inspected observations.csv directly to confirm which vitals LOINC codes
  are actually present before writing ADR-017 (Synthea-only, no Kaggle
  supplement) — heart rate/BP/glucose are common (~13k rows each across 1171
  patients), SpO2/temperature are rare (~5% of encounters). Wrote
  fetch_synthea.py + seed_synthea.py, ran them end-to-end: 200 patients → 50
  facilities, 50 providers, 953 health_readings. Found and fixed a real bug
  during verification (provider name cleaning left embedded digits, e.g.
  "Tomas436 Sauer", because Synthea's provider NAME field isn't pre-split
  like patients' FIRST/LAST). Logged ADR-016 (blood_pressure split into
  systolic_bp/diastolic_bp — a genuine schema refinement, not just an
  implementation detail) and ADR-017 in deccission.md; added backend-schema.md
  §6 documenting the Synthea→schema mapping; updated impmemnentaion-plan.md
  Phase 1 status and infra/README.md with DB setup steps.
WHAT CHANGED: Repo now has a full data layer (models + migration + seed
  tooling), not just an empty scaffold. Not yet committed/pushed this half of
  the session.
WHAT WORKED: Full pipeline verified end-to-end on SQLite: model imports,
  mapper configuration, migration up/down, and the Synthea seed script all
  ran successfully with sane output (spot-checked actual row data, not just
  exit codes — e.g. confirmed vitals ranges were physiologically plausible).
WHAT DID NOT WORK / COULD NOT BE VERIFIED: No real PostgreSQL run — this
  sandbox has neither Docker nor a way to install Postgres without a sudo
  password. SQLite is a reasonable logical stand-in for "does this code run
  and produce sane output" but is NOT the same as verifying Postgres-specific
  behavior (native ENUM types, etc.). Do not report the Phase 1 exit
  criteria ("schema migrated into a running PostgreSQL container") as fully
  met — say SQLite-verified, Postgres-pending, same framing as Phase 0's
  Docker gap.
CURRENT STATE: Phase 1 functionally complete pending (a) a real Postgres run
  and (b) pushing this session's commit to GitHub.
NEXT ACTION: Commit this session's Phase 1 work; ask the user how they want
  to push; then start Phase 2 (JWT auth + Module 1 CRUD endpoints per
  api-spec.md §2-3).
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
