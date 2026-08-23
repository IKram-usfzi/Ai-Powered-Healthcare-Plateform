# User Guide

**Related:** `api-spec.md` §8 (role–permission summary), `UIUX.md`

How to use GlobalCare as each of the four roles. Assumes the platform is running (`installation-guide.md`) at http://localhost:5173.

## Logging in

Go to http://localhost:5173/login and sign in with your email/password. After login you're redirected to the first screen your role can actually access (`frontend/src/auth/defaultRoute.js`): Executive → Executive Overview (`/dashboard/executive`); Administrator → Unified dashboard (`/dashboard`); Doctor → Patients (`/patients`, no dashboard access); Patient → Appointments (`/appointments`).

Demo accounts (`backend/scripts/seed_dev_users.py`), all password `ChangeMe123!`:

| Role | Email |
|---|---|
| Administrator | `admin@globalcare-demo.com` |
| Executive | `executive@globalcare-demo.com` |
| Doctor | `doctor@globalcare-demo.com` |
| Patient | `patient@globalcare-demo.com` (assigned to the demo doctor) |

The top nav only shows links your role can actually use — a Patient sees Appointments/Telemedicine only; a Doctor sees Patients/Appointments/Telemedicine/Monitoring/Analytics; Administrator/Executive additionally see the dashboards.

## Patient

A Patient can:

- **Book an appointment** — Appointments screen (`/appointments`), "+ Book Appointment". Since patients can't browse the full provider directory (`GET /providers` is Administrator/Executive only), the form asks for a provider ID rather than a picker — ask your care team for it.
- **View and manage appointments/consultations** — Appointments and Telemedicine screens (`/appointments`, `/telemedicine`) show your own bookings and their status.
- **Submit vitals readings** — `POST /monitoring/readings` (heart rate, blood pressure, SpO2, temperature, glucose) via the API; an abnormal reading raises an alert for your care team automatically (`flow.md` §3). No dedicated vitals-submission screen yet — this is the one still API-only.
- **View your own records** — reading history and AI risk prediction history (`GET /monitoring/readings/{patientId}`, `GET /ai/predictions/{patientId}`) — always scoped to your own data only.

## Doctor

A Doctor can, all through real screens now (`/patients`, `/appointments`, `/telemedicine`, `/monitoring`, `/analytics`):

- **View their assigned patients** — Patients screen; click a row to expand recent vitals, consultations, and AI predictions inline.
- **View their schedule and update appointment status** — Appointments screen.
- **Record a consultation** — Telemedicine screen's "Awaiting Consultation" queue; recording one automatically marks the appointment `completed` (`flow.md` §2).
- **View and acknowledge alerts** for their assigned patients — Monitoring screen.
- **Request an AI risk assessment** for an assigned patient — Analytics screen; select a patient, "Run New Assessment" returns a risk category, confidence score, and a recommendation that always states it requires clinical judgement, never a diagnosis (`PRD.md` §7).
- Everything above is scoped to the doctor's own assigned patients — a doctor cannot read or act on a patient not assigned to them (`Security.md` §3), and the UI reflects that (e.g. the Patients screen only ever lists your own assigned patients).

## Administrator

An Administrator sees everything a Doctor sees (Patients/Appointments/Telemedicine/Monitoring/Analytics, unscoped — all patients, all alerts) plus the Unified dashboard (`/dashboard`) and Healthcare Operations view (`/dashboard/operations`). Consultation-recording, alert-acknowledgement, and AI-assessment actions stay Doctor-only even for Administrators, matching `api-spec.md`'s role table — an Administrator can *see* everything but only *acts* clinically where the API allows it. Full operational detail (registering patients/providers/facilities, running reports, seed scripts) is in `admin-guide.md`.

## Executive

An Executive sees the Executive Overview (`/dashboard/executive`) — the only role with access to this route. It shows:

- KPI cards: Total Patients, Active Providers, Open Alerts, AI Risk Alerts (all real counts, never fabricated — `deccission.md` ADR-022).
- A 7-day Chart.js trend line of vitals readings vs. clinical alerts.
- An AI Risk Assessment panel listing currently flagged high-risk patients.
- Operational Efficiency: today's appointment throughput (Scheduled/Completed/Cancelled).
- **Export Data** — downloads the full executive report (`GET /reports/executive`) as a JSON file.

Executives can also open the Unified dashboard (`/dashboard`) and Healthcare Operations (`/dashboard/operations`) — the nav bar's "Executive"/"Operations" pills switch between views. Executives don't have their own Patients/Monitoring/Analytics screens (those are Administrator/Doctor per `api-spec.md`'s role table) — aggregate versions of that data are what the Executive dashboards already show.
