# Test Execution Summary

**Related:** `Testing-startegy.md` §7, `impmemnentaion-plan.md`
**Purpose:** Running log of test runs (pass/fail counts, notable failures and fixes) as implementation proceeds — the "test execution summary" deliverable for the live demonstration (brief §10, Stage 2).

Most runs below were executed in the authoring sandbox (Python 3.10, no Docker/PostgreSQL —
see `PROJECT_CONTEXT.md`), against SQLite as a logical stand-in. **Phases 0-2 have since been
verified against real Docker Compose + PostgreSQL** on the student's own machine (§ below) —
that's the authoritative run; the SQLite entries stay here as the record of what was checked
before real infrastructure was available.

## Phase 0 — Foundation

| Check | Result |
|---|---|
| `uvicorn app.main:app` boots, `GET /api/v1/health` | ✅ `{"status":"ok"}` |
| `/docs` (Swagger) loads | ✅ HTTP 200 |
| `npm install && npm run dev` (frontend) | ✅ served, fetched live backend health |
| `mkdocs build --strict` | ✅ zero warnings |

## Phase 1 — Data & Domain Modeling

| Check | Result |
|---|---|
| `configure_mappers()` (all 9 models) | ✅ no relationship errors |
| `alembic upgrade head` / `downgrade base` | ✅ clean both directions |
| `seed_synthea.py --patients 200 --max-readings 5` | ✅ 50 facilities, 50 providers, 200 patients, 953 health_readings |

## Phase 2 — Module 1 (Patient & Provider Management)

**Manual end-to-end walkthrough** (live server, curl), 2026-08-22:

| Step | Result |
|---|---|
| Admin login | ✅ 200 |
| `GET /auth/me` | ✅ 200 |
| `POST /auth/refresh` | ✅ 200 |
| `POST /facilities` | ✅ 201 |
| `POST /providers` | ✅ 201 |
| `POST /patients` | ✅ 201 |
| `POST /providers/{id}/assign-patient` | ✅ 200 |
| `GET /patients/{id}` | ✅ 200 |
| `GET /reports/registration` | ✅ 200, counts matched inserted data exactly |
| New provider can log in with their set password | ✅ 200 |
| Doctor's `GET /patients` scoped to assigned patients only | ✅ returned exactly 1 (the assigned one) |
| Doctor `POST /facilities` (role denial) | ✅ 403 |
| No token on `GET /patients` | ✅ 401 |
| Doctor `GET /reports/registration` (role denial) | ✅ 403 |

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **24 passed, 0 failed.**

- `test_health.py` — 1 test
- `test_auth.py` — 7 tests (login success/failure/unknown-email, `/me` auth required, refresh flow, refresh rejects an access token used in place of a refresh token)
- `test_patients.py` — 8 tests (admin CRUD, 404, role denial, patient self-access, patient blocked from another patient's record, unauthenticated 401, doctor list scoped to assigned patients)
- `test_providers.py` — 6 tests (role denial, create + login, duplicate-email 409, list role denial, assign-patient, assign to unknown provider 404)
- `test_reports.py` — 2 tests (role denial, report counts match real inserted data)

**Bugs found and fixed during this phase** (see `deccission.md` for the ADRs where applicable):

1. `patients.assigned_provider_id` didn't exist — `api-spec.md`'s assign-patient endpoint had nothing to write to (ADR-018).
2. All timestamp columns were timezone-naive while every default value was timezone-aware — a latent PostgreSQL correctness bug (ADR-019).
3. `email-validator` rejects `.test`/`.local` as reserved special-use domains — seed data emails switched to `@globalcare-demo.com`.
4. A stale SQLite file descriptor from an earlier manual test server produced a transient "readonly database" error — sandbox process-management artifact, not an application bug; resolved by fully stopping old processes before restarting.

**Lint/format:** `ruff check .` — clean. `black --check .` — clean.

## Real Docker Compose + PostgreSQL run (student's machine, 2026-08-22)

First run against actual infrastructure rather than SQLite. Two real bugs surfaced immediately
and were fixed on the spot:

1. **`backend/Dockerfile` only copied `app/`** — `alembic.ini`, `alembic/`, and `scripts/` had
   been added in Phases 1-2 but the Dockerfile was never updated, so `docker compose exec backend
   alembic ...` and the seed scripts failed with "file not found" inside the container. Fixed:
   Dockerfile now copies all three. Also fixed a related latent bug this surfaced: the Synthea
   data directory lives at `<repo-root>/data/`, outside the `backend/` Docker build context, so
   the scripts' relative-path logic would have resolved to the wrong location even after the
   Dockerfile fix — added a `SYNTHEA_DATA_DIR` env var (bind-mounted `../data:/data` in
   `docker-compose.yml`) so the scripts find the right path in both local and containerized runs.
2. **`passlib==1.7.4` (unmaintained since 2020) incompatible with `bcrypt>=4.1`** — `bcrypt`
   wasn't pinned in `requirements.txt`, so `pip install` picked a version too new for passlib's
   backend-detection code (`AttributeError: module 'bcrypt' has no attribute '__about__'`),
   breaking every password hash/verify call. Worked in the authoring sandbox purely by luck (an
   older `bcrypt` had been installed there at a different time) — a textbook case for why
   `developement-rules.md` §7 requires pinned dependencies. Fixed: pinned `bcrypt==4.0.1`.

After both fixes, rebuilt and re-ran clean:

| Step | Result |
|---|---|
| `docker compose up -d` (postgres, redis, backend, frontend) | ✅ all 4 healthy/started |
| `alembic upgrade head` against real PostgreSQL | ✅ (idempotent on re-run — schema already applied) |
| `seed_dev_users.py` (uses the now-fixed bcrypt) | ✅ both dev users created |
| `seed_synthea.py --patients 200 --max-readings 5` | ✅ 50 facilities, 50 providers, 200 patients, 953 health_readings — identical counts to the SQLite dry-run |
| Frontend (`localhost:5173`) fetching live backend health | ✅ "Backend API status: ok" |
| `POST /auth/login` against real Postgres-backed data | ✅ valid access + refresh JWT returned |

This closes the "SQLite-verified, Postgres-pending" caveat that had applied to every phase status
above — Phases 0-2 are now verified against the actual mandatory deployment path (Docker Compose),
not just simulated.

## Phase 3 — Module 2 (Telemedicine Appointment & Consultation)

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **34 passed, 0 failed** (10 new tests
in `test_appointments.py`, plus the 24 from Phase 2 unaffected).

- Patient books for self / admin books on behalf of a patient / doctor cannot book (role denial)
- Appointment list scoping per role (admin sees all, doctor sees only their own, patient sees only their own)
- Appointment status update: doctor can only update their own appointments (403 otherwise), 404 on unknown id
- Consultation lifecycle: wrong doctor denied (403), correct doctor succeeds (201) and the appointment auto-completes, duplicate consultation rejected (409), patient role denied entirely (403)
- Consultation history: patient sees only their own (403 on another patient's), doctor scoped to their own appointments, admin sees all
- Provider schedule: doctor sees only their own (403 on another provider's), admin sees any, 404 on unknown provider
- Appointment report: role denial for doctor (403), counts match real inserted data

**Real Docker Compose + PostgreSQL run**, 2026-08-22 — backend container restarted to pick up the
new code (bind-mounted `app/`, no rebuild needed), then a full live walkthrough via curl:

| Step | Result |
|---|---|
| `GET /openapi.json` — confirms all 5 new endpoints live | ✅ matches `api-spec.md` §4 exactly |
| Admin creates facility/provider/patient, books appointment | ✅ 201 each |
| Doctor login | ✅ 200 |
| `GET /providers/{id}/schedule` (doctor, own) | ✅ 200, shows the booked appointment |
| `PATCH /appointments/{id}/status` → `in_progress` (doctor) | ✅ 200 |
| `POST /consultations` (doctor) | ✅ 201, appointment auto-completed (verified via re-fetch) |
| `GET /consultations/{patientId}` | ✅ 200, correct summary/recommendations, correctly scoped (not mixed with other patients') |
| `GET /reports/appointments` | ✅ 200, counts matched real inserted data exactly |
| `GET /reports/appointments` as doctor (role denial) | ✅ 403 |

No new bugs found by this run — everything worked on the first try. Ran twice total (once per
verification pass); the second run's doctor email collided with the first (409, expected/correct
uniqueness enforcement), harmless test-script artifact, not a code issue.

**Lint/format:** `ruff check .` — clean. `black --check .` — clean.

## Phase 4 — Module 3 (Remote Patient Monitoring)

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **53 passed, 0 failed** (12 new tests:
8 in `test_vitals.py`, 4+ in `test_monitoring.py`, using an in-memory `FakeRedis` — see
`tests/conftest.py` — since the pytest environment has no real Redis server).

- Threshold unit tests: normal reading → no alert; graduated severity (medium/high/critical) for heart rate, SpO2, temperature, glucose
- Only the Patient role can ingest readings (role denial for others); 400 if the caller has no linked patient record
- **The exact Phase 4 exit criteria**: 3 abnormal readings submitted in a row for the same patient produce **exactly 1** alert (Redis-key dedup) — `test_abnormal_reading_produces_exactly_one_alert_deduped`
- Reading history access scoping (self, assigned doctor, denied for others)
- Alert list scoping (doctor sees only their assigned patients' alerts, role denial for patients)
- Acknowledge: doctor can only acknowledge their own patients' alerts (403 otherwise), 404 on unknown alert id, acknowledged alerts still appear in the "active" list (only `resolved` is excluded)

**A real bug found and fixed before this phase could even be tested end-to-end:** `POST /patients`
(Administrator-only) had no way to create a linked login — `PatientCreate` only had demographic
fields. Every "self (Patient)" access path `api-spec.md`'s role tables promise (this phase's own
`POST/GET /monitoring/readings` included) was unreachable via the documented API. Fixed as ADR-020
— `PatientCreate` now optionally accepts `email`/`password`, mirroring `ProviderCreate`.

**Real Docker Compose + PostgreSQL + Redis run**, 2026-08-22 — backend container restarted
(bind-mounted `app/`, no rebuild) after each code change, then a full live walkthrough via curl
against the **real** Redis container (not the test suite's fake):

| Step | Result |
|---|---|
| `GET /openapi.json` — confirms all 4 new endpoints live | ✅ matches `api-spec.md` §5 exactly |
| Admin creates facility/provider/patient **with a login** (ADR-020) and assigns | ✅ 201/201/201/200 |
| Patient logs in | ✅ 200, valid JWT |
| Patient submits a normal reading | ✅ 201, stored |
| Doctor checks alerts — none yet | ✅ `[]` |
| Patient submits 3 abnormal readings in a row | ✅ 201 × 3 |
| Doctor checks alerts | ✅ **exactly 1** alert, severity `critical` — real Redis dedup confirmed, not simulated |
| Reading history for the patient | ✅ 4 readings total (all stored regardless of alert dedup) |
| Doctor acknowledges the alert | ✅ 200, status → `acknowledged` |

No bugs found by this run itself — the ADR-020 gap was caught and fixed beforehand, precisely by
trying to exercise the Patient role rather than assuming the spec's role table was already
achievable.

**Lint/format:** `ruff check .` — clean. `black --check .` — clean.

## Phase 5 — Module 4 (AI-Assisted Health Risk Assessment)

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **65 passed, 0 failed** (12 new
tests: `test_risk_features_and_labels.py` unit tests + `test_ai.py` router tests, run against the
real trained model artifact committed under `backend/app/ml_models/`).

- Feature extraction order matches training exactly (`age_years, heart_rate, systolic_bp, diastolic_bp, spo2, temperature, glucose`)
- Risk-score bucketing unit tests (normal → low, elderly + multiple abnormal vitals → high, mild deviation → moderate)
- Only the Doctor role can request an assessment; must be assigned to the patient (403 otherwise); 404 for an unknown patient; 400 if the patient has no vitals recorded yet
- A successful assessment returns a valid category/confidence/model_version, and the recommendation text always mentions "clinical judgement"
- Prediction history: doctor (assigned), patient (self), and denial for an unrelated patient
- `GET /ai/model/metadata`: role denial for non-admins, correct fields for admin

**A real bug found by the Docker run itself, not caught by pytest:** `scripts/train_risk_model.py`
computed the AI evaluation report's output path the same way the Phase 1 Synthea-data path bug
did — relative to the script's own location, assuming a `repo-root/backend/scripts/...` depth
that doesn't exist inside the container (`WORKDIR /app` represents `backend/` directly). The
report silently landed at a container-only `/docs/ai-evaluation-report.md`, invisible on the host
and lost on container restart. Fixed the same way as `SYNTHEA_DATA_DIR`: a `DOCS_DIR` env var
(default: the local relative path, unchanged for non-Docker use) plus a `../docs:/docs` bind
mount in `docker-compose.yml`.

**Model training run against real Postgres data** (`docker compose exec backend python
scripts/train_risk_model.py`), 2026-08-22:

| Metric | Value |
|---|---|
| Dataset | 957 `health_readings` rows (real seeded Postgres data, not SQLite) |
| Label distribution | low: 889, moderate: 65, high: 3 |
| Accuracy | 0.995 |
| Precision (macro) | 0.643 |
| Recall (macro) | 0.667 |
| F1 (macro) | 0.654 |

The `high` category's per-class metrics are 0 (only 1 example landed in the 192-row test split)
— documented transparently as a data-imbalance limitation in `docs/ai-evaluation-report.md`
rather than hidden; `low`/`moderate` perform well (0.93-1.00 precision/recall). Cross-Python-
version compatibility confirmed: the model was trained under the container's Python 3.11 and
loaded successfully by the pytest suite running under this environment's Python 3.10.

**Real Docker Compose + PostgreSQL run** (full API walkthrough via curl), 2026-08-22:

| Step | Result |
|---|---|
| `GET /ai/model/metadata` (admin) | ✅ 200, real training metrics returned |
| Admin creates facility/provider/patient-with-login, assigns | ✅ 201 × 3, 200 |
| Patient submits vitals | ✅ 201 |
| Doctor runs `POST /ai/risk-assessment` | ✅ 201, `risk_category: "low"`, `confidence_score: 0.67`, recommendation text present |
| `GET /ai/predictions/{patientId}` (doctor) | ✅ 200, 1 prediction |
| `GET /ai/predictions/{patientId}` (patient, self) | ✅ 200 |
| `GET /ai/model/metadata` as doctor (role denial) | ✅ 403 |

**Lint/format:** `ruff check .` — clean. `black --check .` — clean.

## Phase 6 — Module 5 (Executive Dashboard)

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **72 passed, 0 failed** (7 new tests:
`test_dashboard.py`, using a `_seed_dashboard_data` helper that builds a full facility/provider/
patient/appointment/reading/alert/prediction chain).

- `GET /dashboard/overview`: role denial for a non-admin/non-executive user; reflects real seeded
  patient/appointment/monitoring/alert/prediction counts
- `GET /dashboard/trends`: Executive-only (403 for Administrator); returns exactly 7 days,
  including today's seeded activity
- `GET /dashboard/provider-activity`: reflects real per-provider appointment/patient counts
- `GET /reports/executive`: Executive-only; composes overview + trends + provider-activity
  correctly

**A real bug found while writing the aggregation query, not caught by manual review:**
`Alert.severity == "critical"` compared the enum column against a bare string, which SQLAlchemy's
`Enum` type does not match correctly — fixed to `Alert.severity == AlertSeverity.CRITICAL`.

**Lint/format:** `ruff check .` — clean (after reformatting a >100-char line in `dashboard.py`).
`black --check .` — clean.

**Real Docker Compose + PostgreSQL + frontend run** (browser automation against
`http://localhost:5173`, backend at `http://localhost:8000`), 2026-08-22, real seeded data (204
patients, 54 providers):

| Step | Result |
|---|---|
| Login as `administrator` demo user | ✅ redirected to Unified dashboard (`/dashboard`) |
| Login as `executive` demo user | ✅ redirected to Executive Overview (`/dashboard/executive`) |
| Unified dashboard KPIs | ✅ Total Patients 204, Active Monitoring 2, High Risk 0, real appointment count |
| Executive Overview KPIs + Chart.js trend line | ✅ real 7-day vitals/alerts trend rendered (canvas confirmed present, 732×288) |
| Executive Overview → AI Risk Assessment panel | ✅ real `top_risk_patients` from live data (empty state correct: 0 high-risk) |
| Executive Overview → Operational Efficiency | ✅ real `appointments_today_by_status` breakdown (Scheduled/Completed/Cancelled) |
| Healthcare Operations dashboard | ✅ real busiest-providers table + provider roster + alerts panel (403-graceful for Executive role on `/monitoring/alerts`) |
| `ProtectedRoute`: administrator → `/dashboard/executive` | ✅ redirected back to `/dashboard` (role not permitted) |
| Executive-only "Export Data" button (Unified dashboard) | ✅ `GET /reports/executive` → 200, JSON download triggered |
| `npm run lint` (frontend) | ✅ 0 errors (after fixing the ESLint config — see below) |

**Two real infrastructure bugs found and fixed during this verification:**

1. **Stale frontend dev config (bind-mount gap):** `docker-compose.yml`'s `frontend` service only
   bind-mounted `src/` and `index.html`, not `tailwind.config.js`, `postcss.config.js`, or (found
   later, same root cause) `eslint.config.js` — so the running container kept using the config
   baked into the image at build time. Editing these files on the host had no effect until they
   were added to the service's `volumes:` list and the container recreated
   (`docker compose up -d --no-deps frontend`). Same class of bug as the Phase 1
   `SYNTHEA_DATA_DIR` / Phase 5 `DOCS_DIR` path issues, this time for dev tooling instead of a
   script path.
2. **Stale backend container after a schema field addition:** the frontend briefly crashed
   (`Cannot read properties of undefined (reading 'completed')`) because
   `appointments_today_by_status` had been added to the backend code but the `backend` container
   was never restarted — uvicorn runs without `--reload` in this deployment. Fixed with
   `docker compose restart backend`; hardened the frontend defensively with optional chaining
   (`overview.appointments_today_by_status?.completed ?? 0`) regardless.
3. **ESLint config missing browser globals and JSX-usage detection:** `eslint.config.js` had no
   `languageOptions.globals` (so `fetch`, `localStorage`, `document`, `Blob`, `URL` all flagged as
   undefined) and didn't extend `eslint-plugin-react`'s recommended rules (so every component
   import used only in JSX was flagged as unused). Fixed by adding `globals.browser` and
   `react.configs.recommended.rules` to the config, plus the missing bind mount from bug #1.

## Phase 7 — Observability & Security Hardening

**Automated suite** (`cd backend && pytest -q`), 2026-08-22: **77 passed, 0 failed** (5 new tests:
`test_opa_client.py`, covering the `OPAClient`'s allow/deny/fail-closed behavior against a mocked
`httpx.post`). Reinstalling `requirements.txt` pinned versions was required first — see "A real
environment-drift bug" below.

**Rego unit tests** (`opa test infra/opa/policies -v`, via containerized
`openpolicyagent/opa:0.70.0`), 2026-08-22: **11/11 passed** — `allow_role` (in/not-in the allowed
list, multi-role lists, empty list) and `allow_patient_access` (administrator/executive full
access, patient self-only, doctor assigned-only, doctor denied on an unassigned or null-provider
patient).

**Lint/format:** `ruff check .` — clean. `black --check .` — clean.

**A real environment-drift bug found while installing the new Prometheus dependency:** this
sandbox's host Python has, over the course of the session, drifted to unpinned package versions
newer than `requirements.txt` (FastAPI 0.141.1 vs. the pinned 0.115.6) — a pre-existing gap between
what host-side `pytest` runs were actually testing against and what the Docker image installs.
Installing `prometheus-fastapi-instrumentator==7.0.0` (which caps `starlette<1.0.0`) forced pip to
downgrade the host's starlette to 0.52.1, which is incompatible with the drifted FastAPI 0.141.1 —
59 of 77 tests failed with `AttributeError: '_IncludedRoute' ...`. Not a real application bug: the
Docker image builds `requirements.txt` fresh in an isolated layer and was never affected. Fixed by
reinstalling `pip install -r requirements.txt` on the host to realign it exactly with the pinned
versions, restoring full consistency between host-side test runs and the Docker image (72 passed
again immediately after).

**Real Docker Compose run** (all 7 services: postgres, redis, opa, backend, prometheus, grafana,
frontend), 2026-08-22:

| Step | Result |
|---|---|
| `docker compose up -d` | ✅ all 7 containers started, postgres/redis healthy |
| `GET /metrics` (backend) | ✅ 200, Prometheus text format, real process/request metrics |
| `POST /v1/data/globalcare/authz/allow_role` (OPA, admin allowed) | ✅ `{"result": true}` |
| `POST /v1/data/globalcare/authz/allow_role` (OPA, patient denied) | ✅ `{"result": false}` |
| Login as administrator → `GET /reports/registration` | ✅ 200 (real OPA decision, not FakeOPA) |
| Login as executive → `POST /patients` (admin-only) | ✅ 403 (real OPA decision denies as expected) |
| Login as executive → `GET /dashboard/trends` (executive-only) | ✅ 200 |
| Prometheus target health (`/api/v1/targets`) | ✅ `backend:8000` reports `health: "up"` |
| Prometheus query `sum(http_requests_total)` after generating traffic | ✅ real non-zero count (148) |
| Grafana `/api/health` | ✅ `{"database":"ok"}` |
| Grafana provisioned datasource (`/api/datasources`) | ✅ Prometheus datasource present, `isDefault: true` |
| Grafana provisioned dashboard (`/api/search`) | ✅ `GlobalCare API` dashboard present at `/d/globalcare-api` |
| Grafana → Prometheus proxy query (`/api/datasources/proxy/uid/prometheus/...`) | ✅ real live data returned, matching the direct Prometheus query |

**Trivy scan** (`infra/trivy_scan.sh`, containerized `aquasec/trivy:0.58.0`, no local install),
2026-08-22 — full report: `docs/security-scan-report.md`.

First run (before dependency fixes):

| Image | Critical | High | Medium | Low |
|---|---|---|---|---|
| `infra-backend:latest` | 4 | 60 | 75 | 71 |
| `infra-frontend:latest` | 9 | 72 | 142 | 85 |

Two directly-pinned backend dependencies had CVEs with available fixes: `python-jose` (CVE-2024-33663,
CRITICAL, fixed in 3.4.0) and `python-multipart` (3 CVEs, all fixed by 0.0.30). Bumped to
`python-jose==3.5.0` and `python-multipart==0.0.32` (`backend/requirements.txt`), reinstalled,
re-ran the full pytest suite (77/77 still passing — no behavior change to JWT issuance/verification
or form parsing), rebuilt the backend image, and re-scanned:

| Image | Critical | High | Medium | Low |
|---|---|---|---|---|
| `infra-backend:latest` | 3 | 57 | 73 | 68 |
| `infra-frontend:latest` | 9 | 72 | 142 | 85 |

Both target CVEs confirmed gone from the report. Remaining backend findings are Debian OS packages
(`perl-base`, `util-linux` family, `openssl`, etc. — no upstream fix available yet at scan time) and
`starlette==0.41.3`, which stays pinned for FastAPI 0.115.6 compatibility (ADR-025's default metric
set assumes this FastAPI/starlette pairing). Frontend findings are almost entirely the Debian/Go
base image and Vite's own transitive npm dependency tree (`tar`, `minimatch`, `brace-expansion`,
`cross-spawn`, `glob`, `sigstore`) — a major Vite version bump was judged out of scope for this pass
given the risk to the Tailwind/PostCSS pipeline (ADR-015) for a POC with synthetic data only.
Documented transparently in `docs/security-scan-report.md` rather than chased to zero, consistent
with this project's practice of reporting real limitations (`docs/ai-evaluation-report.md`'s thin
`high`-risk class).

## Phase 8 — AWS Deployment (Terraform IaC, not applied)

**`terraform fmt -check -diff`** (`infra/terraform/`, via the containerized `hashicorp/terraform:1.9`
image, no local install), 2026-08-23: found one misaligned file (`vpc.tf`), fixed with `terraform
fmt`; clean on re-check.

**`terraform init -backend=false` + `terraform validate`**, 2026-08-23: init downloaded the AWS
provider (`hashicorp/aws` 5.100.0) and generated `.terraform.lock.hcl`; validate reported **Success —
the configuration is valid.** No AWS credentials were provided or used — `validate` only checks
syntax, type-correctness, and resource/variable references, not against a real AWS account. This is
deliberately as far as verification goes for this phase — see `deccission.md` ADR-027 for why no
`terraform plan`/`apply` was run against a real account.

**Not run (by design):** `terraform plan`/`apply` against a real AWS account, and therefore the
Phase 8 exit criteria itself ("reachable over the internet," "billing verified") — this phase
delivers infrastructure-as-code for future use, not a live deployment (ADR-027).

## Not yet run

- Frontend component tests (React Testing Library) — no test runner configured yet; verification
  for Phases 6-7 relied on the pytest backend suite plus live browser automation / direct HTTP
  verification against real Docker Compose services
- Phase 8's Terraform against a real AWS account (`terraform plan`/`apply`) — deferred until an
  actual AWS deployment is wanted; see `infra/terraform/README.md`
