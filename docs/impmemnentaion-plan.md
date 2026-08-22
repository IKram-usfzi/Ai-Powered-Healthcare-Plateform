# Implementation Plan (Phased Roadmap)

**Related:** `developement-rules.md`, `Testing-startegy.md`
**Status:** Phases 0-4 done and verified against real Docker Compose + PostgreSQL + Redis (2026-08-22) — see status lines below.

## Phase 0 — Foundation
Repo structure, Git/GitHub setup, base Docker Compose skeleton (empty services), README skeleton, MkDocs init, `deccission.md` started, AWS account/budget-alarm setup.
**Exit criteria:** `docker compose up` runs empty scaffolding without error; repo pushed to GitHub.
**Status:** Met. `docker compose up --build` runs all four services (postgres, redis, backend, frontend) cleanly on the student's machine; repo pushed to GitHub. `mkdocs build --strict` passes. AWS budget-alarm setup still unknown/deferred to Phase 8.

## Phase 1 — Data & Domain Modeling
Finalize PostgreSQL schema per `backend-schema.md`; produce Database ERD; obtain/generate the Synthea dataset and map it to the schema; decide on the supplementary Kaggle vitals dataset question from `deccission.md` (ADR-011).
**Exit criteria:** Schema migrated into a running PostgreSQL container; sample Synthea-derived data loaded.
**Status:** Met. `alembic upgrade head` applied cleanly against real PostgreSQL in Docker Compose; `seed_synthea.py --patients 200 --max-readings 5` loaded 50 facilities/50 providers/200 patients/953 health_readings into it (identical counts to the earlier SQLite dry-run). Schema finalized (`backend-schema.md` §6, ADR-016). ADR-011 resolved as ADR-017 (Synthea only, no supplementary Kaggle dataset). ERD already existed as a Mermaid diagram in `backend-schema.md` §1 — no separate diagram file needed yet (Phase 9 exports it).

## Phase 2 — Module 1: Patient & Provider Management
Registration/profile CRUD APIs per `api-spec.md` §3, JWT auth foundation, role model (Patient/Doctor/Admin/Executive), registration reports.
**Exit criteria:** All Module 1 endpoints functional; registration report generated from real inserted data.
**Status:** Met. All `api-spec.md` §2-3 endpoints implemented: `/auth/login`, `/auth/refresh`, `/auth/me`, `/patients` (POST/GET/GET-by-id/PUT), `/providers` (POST/GET), `/providers/{id}/assign-patient`, `/facilities` (POST), `/reports/registration`. JWT auth (access + refresh tokens) with bcrypt password hashing; role checks enforced at the API layer as the Phase 2 "JWT auth foundation" (Phase 7 formalizes this via OPA per ADR-006) — includes the doctor-scoped "only assigned patients" rule from `Security.md` §3 and patient-self-access. Verified three ways: (1) 24 automated pytest tests (`backend/tests/`, `pytest -q` → 24 passed); (2) a full manual curl walkthrough against a live server (SQLite); (3) a real login against the Docker Compose PostgreSQL deployment, returning a valid JWT. ADR-018 (added `patients.assigned_provider_id` — the original schema had no field for the assign-patient endpoint to write to) and ADR-019 (`DateTime(timezone=True)` on every timestamp column) resolved two real gaps found during implementation; a third (missing `alembic.ini`/`alembic/`/`scripts/` in the Docker image, and an unpinned `bcrypt` version incompatible with `passlib`) was found via the real Docker Compose run and fixed — see `test-execution-log.md`. Ruff+Black clean (`ruff check .`, `black --check .`).

## Phase 3 — Module 2: Telemedicine Appointment & Consultation
Scheduling, consultation records, appointment status tracking, provider schedules, operational reports (`api-spec.md` §4).
**Exit criteria:** End-to-end schedule → consult → history flow demonstrable.
**Status:** Met. All `api-spec.md` §4 endpoints implemented: `POST/GET /appointments`, `PATCH /appointments/{id}/status`, `POST /consultations`, `GET /consultations/{patientId}`, `GET /providers/{id}/schedule`, `GET /reports/appointments`. Patients book appointments for themselves; Administrators can book on behalf of any patient. Recording a consultation auto-transitions the appointment to `completed` (PRD §6 Module 2: "record consultation summaries; track appointment status"). Role scoping follows the Phase 2 pattern: a doctor only sees/acts on their own appointments and schedule; consultation history is additionally restricted to the doctor's own appointments with that patient (an extension of `Security.md` §3's assigned-patient rule to the appointment relationship, not just the standing `assigned_provider_id`). Verified two ways: (1) 10 new automated pytest tests (`backend/tests/test_appointments.py`, full suite now 34 passed); (2) a live end-to-end run against the real Docker Compose + PostgreSQL deployment — book → doctor login → view schedule → update status → record consultation (appointment auto-completed) → consultation history → appointment report → role-denial check, all correct, response bodies inspected directly (not just status codes). Ruff+Black clean.

## Phase 4 — Module 3: Remote Patient Monitoring
Vitals ingestion endpoints, abnormal-reading detection rules, clinical alerting, Redis wired in for de-duplication (`api-spec.md` §5, `flow.md` §3).
**Exit criteria:** Simulated abnormal reading correctly produces exactly one alert (de-dup verified).
**Status:** Met. All `api-spec.md` §5 endpoints implemented: `POST /monitoring/readings` (Patient self-submission), `GET /monitoring/readings/{patientId}`, `GET /monitoring/alerts`, `PATCH /monitoring/alerts/{id}/acknowledge`. Threshold-based severity detection (`app/services/vitals.py`) covers all five vitals across three severity tiers. Redis is now actually wired in (previously running in Docker Compose since Phase 0 but unused) — `app/core/redis_client.py` — for exactly the de-dup role ADR-002 scoped it to: a 5-minute per-patient key prevents repeated abnormal readings from spamming duplicate alerts. Implementing this surfaced ADR-020 (`PatientCreate` gains optional `email`/`password`, mirroring `ProviderCreate` — without it, no patient could ever log in to exercise any "self" access path the spec promises). Verified two ways: (1) 12 new automated pytest tests (8 unit tests for the threshold function plus a router suite using an in-memory fake Redis, full suite now 53 passed) — including the exact exit-criteria scenario (3 abnormal readings → exactly 1 alert); (2) a live run against real Docker Compose + PostgreSQL + **real Redis** (not the test fake) — patient creates a login → submits a normal reading (no alert) → submits 3 abnormal readings in a row → doctor sees exactly 1 alert (severity `critical`) → reading history correctly shows all 4 readings → doctor acknowledges the alert. Ruff+Black clean.

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
