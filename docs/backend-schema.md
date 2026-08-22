# Backend / Database Schema

**Related:** `architecture.md`, `api-spec.md`
**Database:** PostgreSQL · **Status:** Design-time schema; DDL/migrations to be produced during implementation.

## 1. Entity-Relationship Overview

```mermaid
erDiagram
    USERS ||--o{ PATIENTS : "may be"
    USERS ||--o{ PROVIDERS : "may be"
    FACILITIES ||--o{ PROVIDERS : employs
    PATIENTS ||--o{ APPOINTMENTS : books
    PROVIDERS ||--o{ APPOINTMENTS : attends
    APPOINTMENTS ||--o| CONSULTATIONS : produces
    PATIENTS ||--o{ HEALTH_READINGS : generates
    HEALTH_READINGS ||--o{ ALERTS : triggers
    PATIENTS ||--o{ PREDICTIONS : "assessed by AI for"
```

## 2. Entities

**users** — authentication & role identity (`patient`, `doctor`, `administrator`, `executive`). Key fields: id, email, password_hash, role, created_at.

**patients** — patient profile (may link to a `users` record). Key fields: id, user_id (nullable), full_name, date_of_birth, gender, contact_info, registered_at.

**providers** — physicians. Key fields: id, user_id, full_name, specialty, facility_id, license_ref (simulated), created_at.

**facilities** — healthcare facilities. Key fields: id, name, type, location.

**appointments** — scheduled telemedicine sessions. Key fields: id, patient_id, provider_id, scheduled_at, status (`scheduled`/`in_progress`/`completed`/`cancelled`), created_at.

**consultations** — record of a completed appointment. Key fields: id, appointment_id, summary, recommendations, created_at.

**health_readings** — simulated vitals from remote monitoring. Key fields: id, patient_id, heart_rate, blood_pressure, spo2, temperature, glucose, recorded_at.

**alerts** — abnormal-reading notifications. Key fields: id, patient_id, reading_id, severity, status (`open`/`acknowledged`/`resolved`), created_at.

**predictions** — AI risk assessment output. Key fields: id, patient_id, risk_category, confidence_score, model_version, recommendation, created_at.

## 3. Relationships Summary

- A patient has many appointments, health readings, and predictions.
- A provider has many appointments and belongs to one facility.
- An appointment produces at most one consultation record.
- A health reading may trigger zero or more alerts (abnormal thresholds).
- Every prediction is tied to exactly one patient and records the model version used, supporting the "prediction history" and "AI evaluation report" deliverables.

## 4. Indexing & Performance Notes

- Foreign keys (`patient_id`, `provider_id`, `appointment_id`, `reading_id`) indexed for join performance.
- `health_readings.recorded_at` and `predictions.created_at` indexed to support time-series queries (trends, dashboards).
- Dashboard aggregate queries are candidates for Redis caching rather than repeated heavy `GROUP BY` queries against PostgreSQL.

## 5. Migration Strategy (planned)

A migration tool (e.g., Alembic, to be confirmed during implementation) will version schema changes; no manual/ad-hoc schema edits against a running environment. Every schema change is expected to be paired with an ADR entry in `deccission.md` if it reflects a design decision (not just a fix).
