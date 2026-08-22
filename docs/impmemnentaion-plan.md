# Implementation Plan (Phased Roadmap)

**Related:** `developement-rules.md`, `Testing-startegy.md`
**Status:** Planning complete; implementation not yet started (per current instruction — documentation first).

## Phase 0 — Foundation
Repo structure, Git/GitHub setup, base Docker Compose skeleton (empty services), README skeleton, MkDocs init, `deccission.md` started, AWS account/budget-alarm setup.
**Exit criteria:** `docker compose up` runs empty scaffolding without error; repo pushed to GitHub.

## Phase 1 — Data & Domain Modeling
Finalize PostgreSQL schema per `backend-schema.md`; produce Database ERD; obtain/generate the Synthea dataset and map it to the schema; decide on the supplementary Kaggle vitals dataset question from `deccission.md` (ADR-011).
**Exit criteria:** Schema migrated into a running PostgreSQL container; sample Synthea-derived data loaded.

## Phase 2 — Module 1: Patient & Provider Management
Registration/profile CRUD APIs per `api-spec.md` §3, JWT auth foundation, role model (Patient/Doctor/Admin/Executive), registration reports.
**Exit criteria:** All Module 1 endpoints functional; registration report generated from real inserted data.

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
