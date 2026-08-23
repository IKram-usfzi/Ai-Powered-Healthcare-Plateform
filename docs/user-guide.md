# User Guide

**Related:** `api-spec.md` §8 (role–permission summary), `UIUX.md`

How to use GlobalCare as each of the four roles. Assumes the platform is running (`installation-guide.md`) at http://localhost:5173.

## Logging in

Go to http://localhost:5173/login and sign in with your email/password. After login you're redirected based on role: Executives land on the Executive Overview (`/dashboard/executive`); everyone else with dashboard access lands on the Unified view (`/dashboard`).

Demo accounts (`backend/scripts/seed_dev_users.py`): `admin@globalcare-demo.com` / `executive@globalcare-demo.com`, both password `ChangeMe123!`. Patients and doctors don't have seeded demo logins by default — an Administrator creates them via `POST /patients` / `POST /providers` with `email`/`password` (see `admin-guide.md`).

## Patient

A Patient can:

- **Book an appointment** — `POST /appointments` (via the API; no dedicated booking UI exists yet — see `PROJECT_CONTEXT.md` §11 for scope notes).
- **Submit vitals readings** — `POST /monitoring/readings` (heart rate, blood pressure, SpO2, temperature, glucose). An abnormal reading raises an alert for your care team automatically (`flow.md` §3).
- **View your own records** — appointments, consultation history, reading history, and AI risk prediction history (`GET /consultations/{patientId}`, `GET /monitoring/readings/{patientId}`, `GET /ai/predictions/{patientId}`) — always scoped to your own data only.

## Doctor

A Doctor can:

- **View their schedule** — `GET /providers/{id}/schedule`.
- **Update an appointment's status and record a consultation** — recording a consultation automatically marks the appointment `completed` (`flow.md` §2).
- **View and acknowledge alerts** for their assigned patients — Healthcare Operations view (`/dashboard/operations`) shows an "Important Alerts" panel; `GET /monitoring/alerts` / `PATCH /monitoring/alerts/{id}/acknowledge`.
- **Request an AI risk assessment** for an assigned patient — `POST /ai/risk-assessment` returns a risk category, confidence score, and a recommendation that always states it requires clinical judgement, never a diagnosis (`PRD.md` §7).
- Everything above is scoped to the doctor's own assigned patients — a doctor cannot read or act on a patient not assigned to them (`Security.md` §3).

## Administrator

An Administrator sees the Unified dashboard (`/dashboard`) and the Healthcare Operations view (`/dashboard/operations`) — role-gated same as Doctor/Executive access, via `ProtectedRoute`. Full operational detail (registering patients/providers/facilities, running reports, seed scripts) is in `admin-guide.md`.

## Executive

An Executive sees the Executive Overview (`/dashboard/executive`) — the only role with access to this route. It shows:

- KPI cards: Total Patients, Active Providers, Open Alerts, AI Risk Alerts (all real counts, never fabricated — `deccission.md` ADR-022).
- A 7-day Chart.js trend line of vitals readings vs. clinical alerts.
- An AI Risk Assessment panel listing currently flagged high-risk patients.
- Operational Efficiency: today's appointment throughput (Scheduled/Completed/Cancelled).
- **Export Data** — downloads the full executive report (`GET /reports/executive`) as a JSON file.

Executives can also open the Unified dashboard (`/dashboard`) and Healthcare Operations (`/dashboard/operations`) — the nav bar's "Executive"/"Operations" pills switch between views.
