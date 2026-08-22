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
