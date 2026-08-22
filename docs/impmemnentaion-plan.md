# Implementation Plan (Phased Roadmap)

**Related:** `developement-rules.md`, `Testing-startegy.md`
**Status:** Phase 0 in progress — see Phase 0 status line below.

## Phase 0 — Foundation
Repo structure, Git/GitHub setup, base Docker Compose skeleton (empty services), README skeleton, MkDocs init, `deccission.md` started, AWS account/budget-alarm setup.
**Exit criteria:** `docker compose up` runs empty scaffolding without error; repo pushed to GitHub.
**Status:** Repo structure, `docker-compose.yml`, backend/frontend skeletons, root README, and MkDocs config are done and verified locally (FastAPI `/api/v1/health` runs and responds; `mkdocs build --strict` passes). Not yet verified: `docker compose up` itself (no Docker in the authoring sandbox — needs a run on the student's own machine) and AWS budget-alarm setup (status unknown, deferred to Phase 8).

## Phase 1 — Data & Domain Modeling
Finalize PostgreSQL schema per `backend-schema.md`; produce Database ERD; obtain/generate the Synthea dataset and map it to the schema; decide on the supplementary Kaggle vitals dataset question from `deccission.md` (ADR-011).
**Exit criteria:** Schema migrated into a running PostgreSQL container; sample Synthea-derived data loaded.
**Status:** Schema finalized (`backend-schema.md` §6, ADR-016), SQLAlchemy models + Alembic migration written and verified against SQLite (no Postgres in the authoring sandbox — needs a real run). Synthea CSV sample obtained and mapped via `backend/scripts/{fetch,seed}_synthea.py`, verified loading 200 patients/50 providers/50 facilities/953 health_readings. ADR-011 resolved as ADR-017 (Synthea only, no supplementary Kaggle dataset). ERD already existed as a Mermaid diagram in `backend-schema.md` §1 — no separate diagram file needed yet (Phase 9 exports it).

## Phase 2 — Module 1: Patient & Provider Management
Registration/profile CRUD APIs per `api-spec.md` §3, JWT auth foundation, role model (Patient/Doctor/Admin/Executive), registration reports.
**Exit criteria:** All Module 1 endpoints functional; registration report generated from real inserted data.
**Status:** Done and verified. All `api-spec.md` §2-3 endpoints implemented: `/auth/login`, `/auth/refresh`, `/auth/me`, `/patients` (POST/GET/GET-by-id/PUT), `/providers` (POST/GET), `/providers/{id}/assign-patient`, `/facilities` (POST), `/reports/registration`. JWT auth (access + refresh tokens) with bcrypt password hashing; role checks enforced at the API layer as the Phase 2 "JWT auth foundation" (Phase 7 formalizes this via OPA per ADR-006) — includes the doctor-scoped "only assigned patients" rule from `Security.md` §3 and patient-self-access. Verified two ways: (1) a full manual curl walkthrough against a live server — admin login → create facility/provider/patient → assign → registration report → doctor login → scoped list → three role-denial checks (403/401/403), all correct; (2) 24 automated pytest tests (`backend/tests/`, `pytest -q` → 24 passed), covering the same flows plus edge cases (404s, duplicate-email 409, unauthenticated 401). `docker compose`/real-Postgres run still pending (no Docker in the authoring sandbox). ADR-018 (added `patients.assigned_provider_id` — the original schema had no field for the assign-patient endpoint to write to) and ADR-019 (`DateTime(timezone=True)` on every timestamp column) resolved two real gaps found during implementation. Ruff+Black clean (`ruff check .`, `black --check .`).

## Phase 3 — Module 2: Telemedicine Appointment & Consultation
Scheduling, consultation records, appointment status tracking, provider schedules, operational reports (`api-spec.md` §4).
**Exit criteria:** End-to-end schedule → consult → history flow demonstrable.

## Phase 4 — Module 3: Remote Patient Monitoring
Vitals ingestion endpoints, abnormal-reading detection rules, clinical alerting, Redis wired in for de-duplication (`api-spec.md` §5, `flow.md` §3).
**Exit criteria:** Simulated abnormal reading correctly produces exactly one alert (de-dup verified).

## Phase 5 — Module 4: AI-Assisted Health Risk Assessment
Dataset preprocessing (Pandas/NumPy), model training (Scikit-learn) on Synthea-derived features, prediction API with confidence scores, prediction history persisted (`api-spec.md` §6, `flow.md` §4).
**Exit criteria:** Model trained and evaluated (see `Testing-startegy.md` §3); prediction endpoint returns category + confidence + recorded history.

## Phase 6 — Module 5: Executive Dashboard
Aggregation endpoints, KPI/trend queries, React + Tailwind + Chart.js implementation of the three dashboard views (Unified/home, Executive Overview, Healthcare Operations) per `UIUX.md` §3 (`api-spec.md` §7, `flow.md` §5).
**Exit criteria:** All three dashboard views reflect live data from all prior modules.
**Status:** Unblocked — UI/UX template received; full spec in `UIUX.md` §3. (Previously blocked pending template delivery.)

## Phase 7 — Observability & Security Hardening
Prometheus metrics instrumentation, Grafana dashboards, OPA policy authoring, Trivy scans wired into the build process (`Security.md`).
**Exit criteria:** Grafana dashboard shows live metrics; unauthorized-role access attempts correctly denied; Trivy scan report produced.

## Phase 8 — AWS Deployment (stretch)
VPC/subnets/security groups, EC2 + Docker Compose, RDS PostgreSQL, budget alarm verification, network diagrams finalized from the real topology (`architecture.md` §5, `TRD.md` §8).
**Exit criteria:** Platform reachable over the internet from the AWS deployment; billing verified within credit/free-tier limits.
**Note:** Not required by the exam brief — documented under "Future Enhancements" if time-constrained.

## Phase 9 — Documentation & Diagrams
All 17 mandatory diagrams (`architecture.md` §6), standards-mapping table (`Security.md`), Installation/Deployment/User/Admin guides, MkDocs site build.
**Exit criteria:** MkDocs site builds cleanly; every diagram matches the actual implementation.

## Phase 10 — Integration Testing, Demo Rehearsal, Viva Prep
End-to-end test pass, test execution summary, AI evaluation report, GitHub repo review pass, rehearse the 15–20 min presentation, 5–10 min live demo, and prepare for the 30–40 min viva (including scenario-based redesign questions: national telemedicine networks, rural healthcare, disaster response, elderly care, international programmes).
**Exit criteria:** Full run-through completed within the exam's time limits; all GitHub repository requirements (brief §11) present.
