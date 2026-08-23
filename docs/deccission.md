# Architecture Decision Records (ADR Log)

Each entry: Decision, Context, Status, Consequences. Status values: Proposed / Accepted / Superseded.

## ADR-001 — Backend framework: FastAPI
**Context:** Need an async-capable Python API framework with built-in OpenAPI docs to satisfy the API documentation deliverable.
**Decision:** Adopt FastAPI for all REST APIs.
**Status:** Accepted.
**Consequences:** Free interactive docs and validation via Pydantic; Installation/Deployment/User guides still need to be written by hand.

## ADR-002 — Primary datastore: PostgreSQL; caching layer: Redis (scoped role)
**Context:** Domain is highly relational; some data (dashboard aggregates, session state, alert de-dup) benefits from a fast ephemeral store.
**Decision:** PostgreSQL is the system of record; Redis is scoped specifically to dashboard KPI caching, monitoring alert de-duplication, and session/rate-limit state.
**Status:** Accepted.
**Consequences:** Redis's role must be visible in the Data Flow Diagrams and defensible in the viva.

## ADR-003 — Healthcare standards: conceptual FHIR alignment, not a deployed FHIR server
**Context:** HAPI FHIR/OpenMRS/OpenEMR are ecosystem references in the brief (§7), not mandatory runtime components; RAM budget is tight, especially on the AWS free-tier profile.
**Decision:** Model core resources (Patient, Observation, Encounter, Practitioner, Appointment) as FHIR-inspired schemas inside FastAPI; document the mapping. Do not containerize HAPI FHIR/OpenMRS/OpenEMR.
**Status:** Accepted.
**Consequences:** Keeps the stack lightweight; reinforced by using Synthea (which outputs native FHIR R4) as the synthetic data source.

## ADR-004 — Deployment: Docker Compose (mandatory), AWS Free Tier (stretch)
**Context:** Exam brief requires Docker Compose deployment on a laptop; the student additionally wants an AWS deployment for portfolio purposes.
**Decision:** Docker Compose remains the required, primary deployment path. AWS EC2 (t2/t3.micro) + RDS PostgreSQL is an additional, non-mandatory stretch deployment documented under "Future Enhancements." K3s/Kind stays optional.
**Status:** Accepted.
**Consequences:** Two deployment profiles must be documented and kept consistent: "local/full" and "AWS free-tier/trimmed."

## ADR-005 — AI approach: lightweight Scikit-learn classifier on Synthea-derived synthetic data
**Context:** No real PHI permitted; Module 4 requires risk categories, confidence scores, and recorded prediction history.
**Decision:** Use Synthea (MITRE) as the primary synthetic data source; train a lightweight classifier (e.g., Logistic Regression or Random Forest) on derived vitals features; store predictions with confidence scores.
**Status:** Accepted (source); model algorithm choice remains open pending Phase 5.
**Consequences:** Model quality is bounded by the synthetic data's realism; output must be framed as decision support, never diagnosis.

## ADR-006 — AuthN/AuthZ: JWT + role-based access via a narrowly-scoped OPA policy set
**Context:** Four roles (Patient, Doctor, Administrator, Executive) require differentiated access to patient data.
**Decision:** FastAPI issues JWTs on login; OPA evaluates a small, explicit set of Rego policies for patient-data access rather than a general policy platform.
**Status:** Accepted.

## ADR-007 — Observability: Prometheus + Grafana, profile-aware
**Context:** Full monitoring stack is heavy relative to both the 8 GB laptop floor and the ~1 GB AWS free-tier instance.
**Decision:** Run full Prometheus + Grafana on the local/full (16 GB) profile; trim to demo-only or omit on the AWS free-tier profile.
**Status:** Accepted.

## ADR-008 — Documentation & diagrams: Markdown/MkDocs + diagrams-as-code
**Context:** 17 mandatory diagrams must stay consistent with an evolving design; binary diagram tools are hard to diff in Git.
**Decision:** Prefer Mermaid/PlantUML for most diagrams; reserve Draw.io for presentation-specific layout needs. Publish docs via MkDocs.
**Status:** Accepted.

## ADR-009 — Security scanning: Trivy in the build/deploy process
**Context:** DevSecOps expectation in the brief.
**Decision:** Run Trivy against built Docker images before/at deployment; capture output as the GitHub "security scan report" deliverable.
**Status:** Accepted.

## ADR-010 — UI/UX sourced from a supplied template
**Context:** Student will provide a UI/UX template rather than have one designed from scratch.
**Decision:** React implementation follows the supplied template once received; no independent UI/UX design work in the interim.
**Status:** Accepted — template received (25-screen "Clinical Precision" design system + "Clinical Precision Mobile" variant). Full breakdown in `UIUX.md`.

## ADR-011 — Synthetic data source: Synthea (primary)
**Context:** Public dataset required, fetched from the internet rather than custom-generated.
**Decision:** Synthea (MITRE) as the primary source, given native FHIR R4 output and no PHI/consent concerns; a supplementary flat Kaggle vitals dataset remains an open option for Module 4 training specifically.
**Status:** Proposed — final call on supplementary source open (see `impmemnentaion-plan.md` Phase 1).

## ADR-012 — Frontend styling/charting stack confirmed from the supplied UI/UX template
**Context:** The supplied template ("Clinical Precision" design system, 25 screens) is built with Tailwind CSS (via CDN, utility classes), Google Fonts (Manrope for headings/KPIs, Inter for body/labels), Material Symbols Outlined icons, and Chart.js (via CDN) for interactive charts (e.g., the Clinical Activity & RPM line chart on the Executive Overview screen). This is more specific than the original TRD, which only named Plotly/Matplotlib for visualization per the exam brief's Python-centric tech stack list.
**Decision:** Adopt Tailwind CSS as the React styling approach and Chart.js as the client-side charting library for all interactive, in-browser dashboard visuals, to match the template exactly. Reserve Plotly/Matplotlib (brief §7) for Python-side outputs that don't need to be interactive React components — e.g., the AI evaluation report, exported/static analytics charts, and any Jupyter-style exploratory analysis during Module 4 development. Material Symbols Outlined is the icon set; Manrope + Inter are the two typefaces, loaded via Google Fonts.
**Status:** Accepted.
**Consequences:** Frontend dependency list grows slightly (Tailwind, Chart.js, Google Fonts, Material Symbols) beyond the original brief's Python-only stack table — this is additive, not a conflict, since Plotly/Matplotlib still satisfy the brief's checklist for report-generation contexts. `TRD.md` and `developement-rules.md` should list these explicitly once implementation starts.

## ADR-013 — Backend ORM & migrations: SQLAlchemy 2.0 + Alembic + psycopg3
**Context:** `backend-schema.md` §5 deferred ORM/migration tooling choice to implementation start (Phase 0/1).
**Decision:** SQLAlchemy 2.0 (declarative models) as the ORM, Alembic for versioned migrations, `psycopg[binary]` (psycopg3) as the PostgreSQL driver.
**Status:** Accepted.
**Consequences:** Standard, well-documented combination; Alembic migrations become the only sanctioned way to change schema in a running environment, per `developement-rules.md` §8.

## ADR-014 — Python lint/format tooling: Black + Ruff
**Context:** `developement-rules.md` §3 left the formatter/linter choice open ("Black + isort + Flake8/Ruff — tool choice confirmed at implementation start").
**Decision:** Black for formatting; Ruff for linting (Ruff's `I` ruleset replaces isort, so no separate isort dependency is needed).
**Status:** Accepted.
**Consequences:** One fewer dependency than a Black+isort+Flake8 combination; config lives in `backend/pyproject.toml`.

## ADR-015 — Frontend build tooling: Vite (npm-installed Tailwind, not CDN)
**Context:** The supplied UI/UX template (`UIUX Design/s*/code.html`) uses Tailwind via CDN `<script>` tags for standalone screen previews (ADR-012). The actual React application needs a real build pipeline.
**Decision:** Use Vite as the React build tool/dev server; install Tailwind CSS as an npm dependency with PostCSS (not the CDN script) for the production React app. The CDN approach in the template files remains fine for the standalone preview screens under `UIUX Design/`, which are reference material, not the shipped app.
**Status:** Accepted.
**Consequences:** Standard, fast dev-server experience (Vite HMR); Tailwind's utility classes and design tokens (Manrope/Inter/Material Symbols, per ADR-012) are preserved identically between the template previews and the real app.

## ADR-016 — `health_readings.blood_pressure` split into `systolic_bp` / `diastolic_bp`
**Context:** `backend-schema.md` originally listed a single `blood_pressure` field. Finalizing the schema for Phase 1 (SQLAlchemy models + Alembic migration) surfaced that a combined field (e.g. `"120/80"` as a string) is awkward for the abnormal-reading threshold checks (Module 3) and the AI risk model's numeric feature set (Module 4) — both need systolic/diastolic as independent numbers.
**Decision:** Store `systolic_bp: int` and `diastolic_bp: int` as two columns instead of one combined `blood_pressure` field.
**Status:** Accepted.
**Consequences:** `backend-schema.md` §2/§6 updated to match; any future API payload for vitals ingestion (`POST /monitoring/readings`, Phase 4) uses `systolic_bp`/`diastolic_bp` as two request fields, not one combined string.

## ADR-017 — Synthea supplementary dataset question (ADR-011) resolved: Synthea only
**Context:** ADR-011 left open whether a supplementary Kaggle vitals dataset was needed alongside Synthea for Module 4 training. Phase 1 requires a decision before the dataset is pulled.
**Decision:** Synthea alone is sufficient — its CSV export's `observations.csv` carries LOINC-coded vitals (heart rate, systolic/diastolic blood pressure, SpO2, body temperature, blood glucose) that map directly onto `health_readings`, and its `conditions.csv`/`patients.csv` provide enough signal for a lightweight risk classifier (Phase 5). No supplementary Kaggle dataset is pulled in.
**Status:** Accepted.
**Consequences:** One data source to document/cite in the AI evaluation report; simpler data-provenance story for the viva. Revisit only if Phase 5 model evaluation shows the feature set is too thin.

## ADR-018 — `patients.assigned_provider_id` added (closes an api-spec/schema gap)
**Context:** Implementing Phase 2's `POST /providers/{id}/assign-patient` (`api-spec.md` §3) and the doctor-scoped access rule in `Security.md` §3 ("a doctor may read/write only their assigned patients' records") surfaced that the original `backend-schema.md` had no field anywhere to persist a patient↔provider assignment — the endpoint existed in the API contract with nothing to write to.
**Decision:** Add a nullable `assigned_provider_id` FK on `patients`, pointing at `providers.id`. One active assigned provider per patient at a time (re-assigning overwrites it); this matches the singular framing of the assign-patient action and PRD §6 Module 1 ("assign physicians"). A many-to-many join table was considered and rejected as unneeded complexity — nothing in the docs calls for a patient having multiple simultaneously-assigned providers.
**Status:** Accepted.
**Consequences:** `backend-schema.md` §2 updated; `providers -> patients` becomes a one-to-many relationship via this FK (in addition to the existing many-to-many-via-appointments relationship, which represents actual visits, not standing assignment). Folded into the single `initial schema` migration (Phase 2) since no earlier migration had been applied to any real deployment yet — see ADR-019.

## ADR-019 — `DateTime(timezone=True)` on every timestamp column
**Context:** Implementing Phase 2 auth (JWT expiry, token issuance) surfaced that all 9 models' timestamp columns (`created_at`, `registered_at`, `recorded_at`, `scheduled_at`) used bare `Mapped[datetime]`, which SQLAlchemy maps to a timezone-naive column by default, while every default value used `datetime.now(timezone.utc)` (timezone-aware) — a real correctness gap for PostgreSQL (`TIMESTAMP WITHOUT TIME ZONE` silently drops/mishandles tz-aware input depending on driver) that would have surfaced later as subtle off-by-timezone bugs.
**Decision:** Every timestamp column explicitly uses `DateTime(timezone=True)` (→ `TIMESTAMPTZ` on PostgreSQL). Because no migration had been applied to any real deployment yet (only disposable local SQLite smoke tests), the two Phase 1/2 migrations were regenerated into one clean `initial schema` migration rather than layered as a third fix-up migration.
**Status:** Accepted.
**Consequences:** All datetimes are stored and compared as UTC-aware consistently between Python and the database; no separate fix-up migration needed since nothing was deployed yet.

## ADR-020 — `PatientCreate` optionally accepts `email`/`password` (closes another api-spec/schema gap)
**Context:** Implementing Phase 4 (Remote Patient Monitoring) and trying to actually exercise `POST /monitoring/readings` (role: Patient only, per `api-spec.md` §5) surfaced that `POST /patients` (Administrator-only, per `api-spec.md` §3) had no way to create a linked login — `PatientCreate` only had demographic fields. Every "self (Patient)" access path that `api-spec.md`'s role tables promise throughout Modules 1-3 (`GET /patients/{id}`, `POST/GET /appointments`, `GET /consultations/{patientId}`, `POST/GET /monitoring/readings/{patientId}`) was consequently unreachable via the documented API — a patient could never actually log in. Same category of gap as ADR-018 (assign-patient), found by trying to exercise the feature rather than just reading the spec.
**Decision:** `PatientCreate` gains optional `email`/`password` fields (must be given together or not at all), mirroring the pattern `ProviderCreate` already uses. When supplied, `POST /patients` creates a linked `User` (role `patient`) the same way `POST /providers` creates one (role `doctor`). Omitting both still works exactly as before — an administrative record with no portal access, matching `patients.user_id`'s original nullable design.
**Status:** Accepted.
**Consequences:** Newly-created patients can now genuinely use every "self" access path in the API. The 200 patients loaded by `seed_synthea.py` remain unlinked (`user_id = NULL`) — that script's job is bulk historical/demo data, not individual portal accounts — so exercising patient-role endpoints in a demo requires creating a patient via `POST /patients` with credentials (or linking one directly in the database), not one of the bulk-seeded ones.

## ADR-021 — AI risk classifier algorithm: RandomForestClassifier, trained on a rule-derived label
**Context:** ADR-005 named Synthea as the data source and left "Logistic Regression or Random Forest" open pending Phase 5. No real clinical outcome labels exist for synthetic patients, so a training label had to be manufactured. `app/services/vitals.py` (Module 3's alert thresholds) was considered as the label source but rejected — reusing it would make the classifier trivially learn to replicate a threshold rule already implemented directly in code, adding no value.
**Decision:** A separate weighted point-score heuristic (`app/services/risk_labels.py`, age + all 5 vitals, structurally different from the alert-threshold logic) generates training labels for a `RandomForestClassifier` (`n_estimators=100`, `max_depth=6`, `class_weight="balanced"`). Trained on one row per `health_readings` entry (not deduplicated per patient) to maximize sample size and representation of the rarer risk categories. Feature extraction (`app/services/risk_features.py`) is shared verbatim between `scripts/train_risk_model.py` (training) and `app/api/v1/ai.py` (inference) to avoid train/serve skew.
**Status:** Accepted.
**Consequences:** Real, measured metrics (accuracy/precision/recall/F1/confusion matrix) rather than a hand-authored classifier, satisfying `Testing-startegy.md` §3 and producing a genuine `docs/ai-evaluation-report.md`. The `high` risk category has very few examples in the current seed data (naturally rare, not a bug) — documented transparently in the evaluation report rather than papered over. Model + metadata are committed to git as build artifacts (`backend/app/ml_models/`) since retraining requires a fully-seeded database; `scripts/train_risk_model.py` regenerates both whenever the data changes meaningfully.

## ADR-022 — Dashboard KPIs: real computable equivalents instead of fabricated template metrics
**Context:** The supplied "Clinical Precision" template (`UIUX Design/s2`, `s17`) includes KPIs and widgets the platform has no backing data for — a "Bed Occupancy" percentage, an appointment "No-Show" rate, provider presence/load indicators, and a pixel-positioned Gantt timeline of appointments. Nothing in `backend-schema.md` tracks beds, and `appointments.status` has no "no-show" value (only scheduled/completed/cancelled, per `api-spec.md` §4) — inventing these numbers would mean displaying data that was never computed from anything real.
**Decision:** Wherever the template assumes untracked data, substitute the closest real, computable equivalent rather than hard-coding or fabricating a plausible-looking number: Active Providers (a real `provider_activity` count) replaces Bed Occupancy; Cancelled (a real status-group count) replaces No-Shows; a real "Busiest Providers Today" table sorted by actual appointment counts replaces the fabricated Gantt timeline; the Provider Roster shows only real specialty/assigned-patient-count fields, dropping the template's fabricated presence/load indicators. Documented per-substitution in `UIUX.md` §5.
**Status:** Accepted.
**Consequences:** Every number rendered in the dashboard is traceable to a real aggregation query (`app/api/v1/dashboard.py`) with nothing invented for visual completeness — consistent with the project's "no fabricated data" discipline established in Phase 4/5 (real Redis de-dup, real trained model metrics). A future phase that adds bed/no-show tracking to the schema could restore the original template widgets without changing this ADR's principle.

## ADR-023 — Frontend dev-tooling config files added to the Docker bind mounts (`tailwind.config.js`, `postcss.config.js`, `eslint.config.js`)
**Context:** `docker-compose.yml`'s `frontend` service originally bind-mounted only `src/` and `index.html` for live-reload dev (Phase 0). Phase 6 needed to iterate on `tailwind.config.js` (design tokens) and later `eslint.config.js` (lint rules) — edits on the host had no effect because the running container kept using whichever version of these files was baked into the image at build time. Same class of bug as the Phase 1 `SYNTHEA_DATA_DIR` / Phase 5 `DOCS_DIR` path issues (`app/` inside the container is `backend/`'s contents directly, not `repo-root/backend/`), recurring here for dev tooling instead of a script path.
**Decision:** Bind-mount every frontend config file a developer might reasonably edit during local development (`tailwind.config.js`, `postcss.config.js`, `eslint.config.js`) alongside `src/` and `index.html`, so `docker compose up` reflects host edits without an image rebuild — matching the project's existing "bind-mount for live dev reload" pattern rather than requiring `docker compose build` for config-only changes.
**Status:** Accepted.
**Consequences:** Config changes take effect after `docker compose up -d --no-deps frontend` (container recreate, not just restart, since Compose only re-reads `volumes:` on recreate) rather than a full image rebuild. Any new frontend config file added later (e.g. `vite.config.js` if it moves out of the image) should follow the same pattern.

## ADR-024 — OPA scope: role-based endpoint access only, fail-closed; row-level checks stay in the API layer
**Context:** ADR-006 committed to "a narrow, explicit set of OPA Rego policies" rather than a general policy platform, and left the exact boundary for Phase 7 to decide. `Security.md` §3 names three example policies ("a doctor may read/write only their assigned patients' records," "an executive may read aggregate data but not individual patient records," "an administrator has full CRUD over registration data"), while `Security.md` §9's threat table separately assigns cross-role data leakage to "row-level authorization checks tied to JWT identity, enforced at the API layer" — i.e. the docs already scope coarse role-gating to OPA and fine-grained per-record checks to the API layer, not to OPA. Rewriting all ~8 existing ad-hoc `assigned_provider_id` comparison call sites (across `patients.py`, `appointments.py`, `monitoring.py`, `ai.py`) into per-request OPA calls would touch nearly every router, adding real risk to a fully-tested (72 tests passing pre-Phase-7) codebase for a change the project's own security design doesn't actually call for.
**Decision:** `app/api/deps.py`'s `require_roles()` — used at every role-gated endpoint — now delegates its allow/deny decision to OPA's `allow_role` Rego rule (`infra/opa/policies/authz.rego`) via a small `OPAClient` (`app/core/opa_client.py`), replacing the previous Python `in` check. OPA fails closed: any error reaching it (timeout, connection refused, non-2xx, malformed response) denies the request rather than allowing it. The row-level "doctor's own assigned patients only" and "patient's own record only" checks remain exactly where `Security.md` §9 puts them — in the API layer — unchanged from Phases 2-6. A second Rego rule, `allow_patient_access`, is authored and unit-tested (`infra/opa/policies/authz_test.rego`, `opa test`) to satisfy `Security.md` §3's named examples and demonstrate the pattern, but is not wired into any call site; it's available for a future phase to adopt if row-level policy centralization becomes worth the added latency/complexity.
**Status:** Accepted.
**Consequences:** Every existing role-gated endpoint (~30+ routes across all 5 modules) is now genuinely OPA-backed with zero per-route code changes, since they all go through the one `require_roles()` dependency. Tests use a `FakeOPA` fixture (`tests/conftest.py`) mirroring the Rego logic exactly, following the same pattern as `FakeRedis` — pytest never needs a running OPA server. A real OPA server is required for the backend to authorize anything in Docker Compose (`OPA_URL` env var, default `http://opa:8181`); if the `opa` service is down, every role-gated request is denied (fail-closed), which is the correct default for a security control but means `opa` is now a hard dependency for the backend to function, not an optional add-on.

## ADR-025 — Metrics library: `prometheus-fastapi-instrumentator`
**Context:** ADR-007 committed to Prometheus + Grafana for observability but left the FastAPI-side instrumentation approach open. Hand-rolling Prometheus counters/histograms around every route would duplicate what a maintained library already does correctly (request count, latency histogram, request/response size, labeled by method/handler/status).
**Decision:** Use `prometheus-fastapi-instrumentator`, which auto-instruments every FastAPI route and exposes `/metrics` in the standard Prometheus text format with one call (`Instrumentator().instrument(app).expose(app, endpoint="/metrics")` in `app/main.py`).
**Status:** Accepted.
**Consequences:** `/metrics` is excluded from the OpenAPI schema (`include_in_schema=False`) since it's an operational endpoint, not an API contract endpoint. The default metric set (`http_requests_total`, `http_request_duration_seconds`, request/response size) drives the Grafana dashboard (`infra/grafana/dashboards/globalcare-api.json`) directly — no custom metric names to keep in sync between the instrumentation code and the dashboard queries.

## ADR-026 — Trivy scan output: parsed JSON → generated Markdown report, mirroring the AI evaluation report pattern
**Context:** ADR-009 committed to Trivy scanning the built images, captured as the GitHub "security scan report" deliverable (exam brief §11). Trivy's native output formats (table, JSON, SARIF) aren't directly suitable as a committed documentation artifact — the table format doesn't summarize well across multiple images, and raw JSON isn't reviewable in a PR or during the viva.
**Decision:** `infra/trivy_scan.sh` runs containerized Trivy (`aquasec/trivy`, no local install needed) against both built images (`infra-backend:latest`, `infra-frontend:latest`), then `infra/generate_security_report.py` parses the JSON output into `docs/security-scan-report.md` — a per-image Critical/High/Medium/Low summary table plus itemized Critical/High findings (CVE, package, installed/fixed version). Same generated-report-from-real-data pattern already used for `docs/ai-evaluation-report.md` (Phase 5).
**Status:** Accepted.
**Consequences:** The report reflects whatever Trivy's vulnerability database currently knows about the pinned base images/dependencies at scan time — findings are documented transparently (consistent with the AI model's thin `high`-risk class being reported rather than hidden) rather than the report being edited to look clean. Re-running `infra/trivy_scan.sh` after any `docker compose build --pull` regenerates the report from scratch; it is not hand-maintained.

## ADR-027 — Phase 8 delivers Terraform IaC only; no live AWS deployment
**Context:** ADR-004 already settled that Docker Compose is the mandatory deployment target and AWS is an optional, non-required stretch (exam brief §4/§11). Phase 8's documented exit criteria (`impmemnentaion-plan.md`) is "platform reachable over the internet from the AWS deployment; billing verified" — a live deployment. The user explicitly scoped this session's Phase 8 work to writing the Terraform for future use, while the actual deployment stays on the local machine via Docker Compose for now (no AWS account spend, no live infrastructure to babysit or forget to tear down).
**Decision:** `infra/terraform/` implements the full topology from `architecture.md` §5 / `TRD.md` §8 (VPC + public/private subnets, security groups, EC2 + Docker Compose app tier, single-AZ RDS PostgreSQL, an `aws_budgets_budget` billing alarm) as real, `terraform validate`-clean code — but it is never `terraform apply`'d as part of this phase. A companion `infra/docker-compose.aws.yml` override (RDS instead of the local `postgres` container; Prometheus/Grafana trimmed per `TRD.md` §8's ~1GB-RAM note) makes the module actually usable later, not just structurally present. Verification for this phase is therefore `terraform fmt`/`validate` plus a dry-run reasoning check of the resource graph, not a live `apply` — deliberately different from every prior phase's "verify against real infrastructure" standard, and called out here so that difference isn't mistaken for lower rigor elsewhere.
**Status:** Accepted.
**Consequences:** Phase 8's documented exit criteria ("reachable over the internet," "billing verified") is *not* met by this session's work — that remains genuinely future work for whoever runs `terraform apply` later, following `infra/terraform/README.md`. `impmemnentaion-plan.md`'s Phase 8 status reflects "IaC authored, not applied" rather than "done," so this isn't misrepresented as a completed live deployment.

## ADR-028 — `diagrams/` moved under `docs/diagrams/`, not left as a repo-root sibling
**Context:** The Phase 0 scaffolding placed a placeholder `diagrams/` directory at the repo root, as a sibling of `docs/` (`mkdocs.yml`'s `docs_dir: docs`). Populating it with the 17 mandatory diagrams (Phase 9) and linking to them from `architecture.md` §6 immediately broke `mkdocs build --strict` — MkDocs validates relative links that look internal against its known documentation files even when the target lives outside `docs_dir`, so every `../diagrams/*.md` link failed strict validation (`impmemnentaion-plan.md` Phase 9's own exit criteria requires "MkDocs site builds cleanly").
**Decision:** Move `diagrams/` to `docs/diagrams/` so the 17 diagram files are genuine MkDocs pages — added to `mkdocs.yml`'s nav under a "Diagrams" section, internal links resolve normally, and `mkdocs build --strict` passes with zero warnings. `architecture.md` §6's links were updated from `../diagrams/...` to `diagrams/...` accordingly.
**Status:** Accepted.
**Consequences:** Diagrams are now a first-class, browsable part of the documentation site (previously they'd have been loose files only reachable via GitHub's own Markdown rendering), consistent with how `ai-evaluation-report.md` and `security-scan-report.md` were added directly under `docs/` in Phases 5 and 7. Any future file meant to be part of the documentation site belongs under `docs/`, not the repo root — `UIUX Design/` and `technology_stack.txt` remain repo-root by original design (raw source material referenced by, not part of, the docs site) and are unaffected by this ADR.

## ADR-029 — Post-completion scope expansion: real Patients/Appointments/Telemedicine/Monitoring/Analytics screens
**Context:** After all 10 phases were complete, the user tested the deployed app and found the top nav's Patients/Appointments/Telemedicine/Monitoring/Analytics links were inert placeholder text — a deliberate Phase 6 scope decision, since the exam brief only mandates the Dashboard (Module 5) for the frontend; the other four modules were API-complete with no dedicated UI. Given the choice (visually disable, remove, leave as-is, or build real screens), the user chose to build real screens.
**Decision:** Build five new screens (`frontend/src/pages/{Patients,Appointments,Telemedicine,Monitoring,Analytics}.jsx`), each directly on that module's existing, already-tested backend API — no new endpoints added. Screens are scoped to match each underlying API's own role restrictions exactly (`api-spec.md`), not just copied from the dashboard's admin/executive gating: Patients/Monitoring/Analytics → Administrator/Doctor; Appointments/Telemedicine → Administrator/Doctor/Patient. `TopNav` filters which links are shown per role, so a role never sees a link it would just get bounced back from. `backend/scripts/seed_dev_users.py` was extended to also create a Doctor and Patient demo login (previously only Administrator/Executive existed), since roughly half of the new screens' actions (recording a consultation, acknowledging an alert, running an AI risk assessment) are Doctor-only and had no way to be demoed at all before this.
**Status:** Accepted.
**Consequences:** Two real, previously-undiscovered bugs surfaced during this work and were fixed: (1) a redirect-loop bug dormant since Phase 6 — `ProtectedRoute`'s denial path and `Login.jsx` both hard-coded `/dashboard` as the universal fallback, but Doctor/Patient roles have no dashboard access, so logging in as either would loop forever; fixed with a shared `frontend/src/auth/defaultRoute.js` mapping each role to a route it can actually reach. Never caught earlier because no Doctor/Patient login existed to trigger it. (2) The Patient appointment-booking form had no way to populate its provider dropdown (`GET /providers` is Administrator/Executive only) — fixed by falling back to a plain provider-ID input for roles without directory access, rather than fabricating a provider list the API doesn't grant them (consistent with this project's "honest data only" standard, ADR-022). Not built, deliberately: a real-time video-call UI (s9/s11 — no WebRTC backend exists; Telemedicine focuses on the real, working part, the consultation queue/recording form) and a separate Patient 360° profile page (s7 — folded into the Patients list's inline row-expand instead).
