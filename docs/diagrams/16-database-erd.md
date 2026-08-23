# 16. Database Entity Relationship Diagram

**Source:** `docs/backend-schema.md` §1–2 (canonical design-level source) and `backend/app/models/*.py` (real SQLAlchemy models, Phase 1). This file adds attribute-level detail matching the actual implementation, not just the design-level entity list.

```mermaid
erDiagram
    USERS ||--o| PATIENTS : "may be"
    USERS ||--o| PROVIDERS : "may be"
    FACILITIES ||--o{ PROVIDERS : employs
    PROVIDERS |o--o{ PATIENTS : "assigned to (ADR-018)"
    PATIENTS ||--o{ APPOINTMENTS : books
    PROVIDERS ||--o{ APPOINTMENTS : attends
    APPOINTMENTS ||--o| CONSULTATIONS : produces
    PATIENTS ||--o{ HEALTH_READINGS : generates
    HEALTH_READINGS ||--o{ ALERTS : triggers
    PATIENTS ||--o{ ALERTS : "has"
    PATIENTS ||--o{ PREDICTIONS : "assessed by AI for"

    USERS {
        int id PK
        string email UK
        string password_hash
        enum role "patient/doctor/administrator/executive"
        datetime created_at
    }
    PATIENTS {
        int id PK
        int user_id FK "nullable, unique"
        string full_name
        date date_of_birth
        string gender
        string contact_info
        datetime registered_at
        int assigned_provider_id FK "nullable — ADR-018"
    }
    PROVIDERS {
        int id PK
        int user_id FK "unique"
        string full_name
        string specialty
        int facility_id FK
        string license_ref "simulated"
        datetime created_at
    }
    FACILITIES {
        int id PK
        string name
        string type
        string location
    }
    APPOINTMENTS {
        int id PK
        int patient_id FK
        int provider_id FK
        datetime scheduled_at "timezone-aware, ADR-019"
        enum status "scheduled/in_progress/completed/cancelled"
        datetime created_at
    }
    CONSULTATIONS {
        int id PK
        int appointment_id FK "unique"
        text summary
        text recommendations
        datetime created_at
    }
    HEALTH_READINGS {
        int id PK
        int patient_id FK
        int heart_rate
        int systolic_bp "ADR-016 — split from blood_pressure"
        int diastolic_bp
        int spo2
        float temperature
        float glucose
        datetime recorded_at
    }
    ALERTS {
        int id PK
        int patient_id FK
        int reading_id FK
        enum severity "low/medium/high/critical"
        enum status "open/acknowledged/resolved"
        datetime created_at
    }
    PREDICTIONS {
        int id PK
        int patient_id FK
        enum risk_category "low/moderate/high"
        float confidence_score
        string model_version
        text recommendation
        datetime created_at
    }
```

All timestamp columns use `DateTime(timezone=True)` (ADR-019). Full field-by-field rationale: `docs/backend-schema.md` §2.
