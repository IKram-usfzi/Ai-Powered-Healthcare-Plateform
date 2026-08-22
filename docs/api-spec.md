# API Specification

**Related:** `architecture.md`, `backend-schema.md`, `Security.md`
**Status:** Design-time contract. FastAPI will auto-generate live OpenAPI/Swagger docs from the implementation; this file is the source-of-truth intent that implementation follows.

## 1. Conventions

- Base path: `/api/v1`
- Format: JSON request/response bodies
- Auth: `Authorization: Bearer <JWT>` on all endpoints except login
- Error shape (planned): `{ "error": { "code": "...", "message": "..." } }`
- Pagination (planned): `?page=&page_size=` with a total-count envelope on list endpoints
- Roles: `patient`, `doctor`, `administrator`, `executive`

## 2. Auth

| Method | Path | Purpose | Roles |
|---|---|---|---|
| POST | `/auth/login` | Authenticate, issue JWT | Public |
| POST | `/auth/refresh` | Refresh access token | Authenticated |
| GET | `/auth/me` | Current user profile & role | Authenticated |

## 3. Module 1 — Patients, Providers, Facilities

| Method | Path | Purpose | Roles |
|---|---|---|---|
| POST | `/patients` | Register patient | Administrator |
| GET | `/patients` | List/search patients | Administrator, Doctor |
| GET | `/patients/{id}` | Patient summary | Administrator, Doctor, self (Patient) |
| PUT | `/patients/{id}` | Update patient profile | Administrator |
| POST | `/providers` | Register physician | Administrator |
| GET | `/providers` | List providers | Administrator, Executive |
| POST | `/facilities` | Register healthcare facility | Administrator |
| POST | `/providers/{id}/assign-patient` | Assign physician to patient | Administrator |
| GET | `/reports/registration` | Registration report | Administrator, Executive |

## 4. Module 2 — Telemedicine Appointments & Consultations

| Method | Path | Purpose | Roles |
|---|---|---|---|
| POST | `/appointments` | Schedule appointment | Patient, Administrator |
| GET | `/appointments` | List/filter appointments | Doctor, Administrator, self (Patient) |
| PATCH | `/appointments/{id}/status` | Update appointment status | Doctor, Administrator |
| POST | `/consultations` | Record consultation summary | Doctor |
| GET | `/consultations/{patientId}` | Consultation history | Doctor, Administrator, self (Patient) |
| GET | `/providers/{id}/schedule` | Provider schedule | Doctor, Administrator |
| GET | `/reports/appointments` | Appointment/operational report | Administrator, Executive |

## 5. Module 3 — Remote Patient Monitoring

| Method | Path | Purpose | Roles |
|---|---|---|---|
| POST | `/monitoring/readings` | Ingest simulated vitals reading | Device/system, Patient |
| GET | `/monitoring/readings/{patientId}` | Patient vitals history | Doctor, Administrator, self (Patient) |
| GET | `/monitoring/alerts` | List active clinical alerts | Doctor, Administrator |
| PATCH | `/monitoring/alerts/{id}/acknowledge` | Acknowledge/resolve alert | Doctor |

## 6. Module 4 — AI Health Risk Assessment

| Method | Path | Purpose | Roles |
|---|---|---|---|
| POST | `/ai/risk-assessment` | Run prediction for a patient's latest data | Doctor |
| GET | `/ai/predictions/{patientId}` | Prediction history | Doctor, Administrator, self (Patient) |
| GET | `/ai/model/metadata` | Model version, training summary | Administrator |

## 7. Module 5 — Executive Dashboard

| Method | Path | Purpose | Roles |
|---|---|---|---|
| GET | `/dashboard/overview` | Registered patients, active appointments, alerts, KPIs | Executive, Administrator |
| GET | `/dashboard/trends` | Healthcare trend analytics | Executive |
| GET | `/dashboard/provider-activity` | Provider/clinical workload | Executive, Administrator |
| GET | `/reports/executive` | Executive report export | Executive |

## 8. Role–Permission Summary

| Role | Own data | Assigned patients | All patients | Admin operations | Executive analytics |
|---|---|---|---|---|---|
| Patient | Read | — | — | — | — |
| Doctor | Read/write own actions | Read/write | — | — | — |
| Administrator | — | — | Read/write | Full | Read |
| Executive | — | — | Read (aggregate) | — | Full |

Enforced via JWT-derived role claims checked against OPA policies (see `Security.md`).
