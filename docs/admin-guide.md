# Administrator Guide

**Related:** `api-spec.md` §3 (Module 1), `Security.md`, `installation-guide.md`

Administrator-specific operations — registering the organization's data, running reports, and the seed/maintenance scripts. General navigation for all roles: `user-guide.md`.

## Registering facilities, providers, and patients

Administrators have full CRUD over registration data (`api-spec.md` §8):

- **Facilities** — `POST /facilities` (name, type, location).
- **Providers** — `POST /providers` (full_name, specialty, facility_id, plus `email`/`password` to create a linked login so the provider can actually sign in as a Doctor).
- **Patients** — `POST /patients` (demographics). `email`/`password` are optional — omit them for a bulk/historical record with no portal access, or include both together to let the patient log in and use "self" access (booking, submitting vitals, viewing their own history). See `deccission.md` ADR-020 for why this pairing exists.
- **Assign a patient to a provider** — `POST /providers/{id}/assign-patient`. One active assignment per patient at a time (re-assigning overwrites it, per `deccission.md` ADR-018).

## Reports

- `GET /reports/registration` — total patients/providers/facilities, patients registered in the last 30 days, unassigned-patient count, providers by specialty.
- `GET /reports/appointments` — operational appointment report.
- `GET /reports/executive` — Executive-only in the UI (the Unified dashboard's "Export Data" button), but the endpoint itself is reachable by any role the API allows; Administrators typically use the Healthcare Operations view instead for day-to-day operations.

## Bulk / demo data (seed scripts)

Run inside the `backend` container (`docker compose -f infra/docker-compose.yml exec backend ...`):

| Script | Purpose |
|---|---|
| `scripts/seed_dev_users.py` | Creates the two demo login accounts (`admin@globalcare-demo.com`, `executive@globalcare-demo.com`, password `ChangeMe123!`). Dev/demo only. |
| `scripts/fetch_synthea.py` | Downloads/prepares the Synthea synthetic patient dataset. |
| `scripts/seed_synthea.py --patients N --max-readings M` | Loads N synthetic patients (default 200) with facilities, providers, and up to M vitals readings each (default 5) into PostgreSQL. These patients have no login by default — they're for populating dashboards/reports with realistic volume, not for demoing "self" access. |
| `scripts/train_risk_model.py` | Retrains the AI risk classifier against current `health_readings` data and regenerates `docs/ai-evaluation-report.md`. Only needed if the underlying data changes meaningfully — the committed model artifact (`backend/app/ml_models/`) is used as-is otherwise. |

## Monitoring the platform itself

As an Administrator you also have access to the operational tooling, not just the application:

- **Healthcare Operations dashboard** (`/dashboard/operations`) — busiest providers today, provider roster, active alerts.
- **Grafana** (http://localhost:3001, `admin`/`admin`) — live request rate, latency, and error-rate metrics for the backend API.
- **Prometheus** (http://localhost:9090) — raw metrics and scrape-target health, if you need to query something Grafana's dashboard doesn't already show.

## Role enforcement

Every admin-gated endpoint is enforced by a real OPA policy decision (`infra/opa/policies/authz.rego`'s `allow_role` rule), not just a client-side check — attempting an admin action while logged in as a non-administrator returns `403 Forbidden` from the API itself, and the frontend's `ProtectedRoute` also redirects away from admin-only pages before the API call would even happen.
