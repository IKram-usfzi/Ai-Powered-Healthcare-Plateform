# Test Execution Summary

**Related:** `Testing-startegy.md` §7, `impmemnentaion-plan.md`
**Purpose:** Running log of test runs (pass/fail counts, notable failures and fixes) as implementation proceeds — the "test execution summary" deliverable for the live demonstration (brief §10, Stage 2).

Every run listed here was executed in the authoring sandbox (Python 3.10, no Docker/PostgreSQL —
see `PROJECT_CONTEXT.md`), against SQLite as a logical stand-in. A real PostgreSQL/Docker Compose
run is still needed on a Docker-capable machine before this can be called fully verified.

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

## Not yet run

- Full `docker compose up` / real PostgreSQL (needs a Docker-capable machine)
- Frontend component tests (React Testing Library) — no frontend UI logic exists yet beyond the Phase 0 placeholder screen
- Trivy scan — no Docker images built yet in a Docker-capable environment
