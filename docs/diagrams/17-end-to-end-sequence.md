# 17. Sequence Diagram — Registration → Appointment → Monitoring → AI Assessment → Executive Reporting

**Source:** `docs/flow.md` §6 (mandatory end-to-end sequence, exam brief §8.17) — converted from ASCII to real Mermaid, spanning all five modules.

```mermaid
sequenceDiagram
    actor Admin as Administrator
    actor Patient
    actor Doctor
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Redis
    participant AI as AI/ML Service
    actor Executive

    Admin->>API: POST /patients (register)
    API->>DB: insert patient
    DB-->>API: patient_id

    Patient->>API: POST /appointments (schedule)
    API->>DB: insert appointment
    DB-->>API: appointment_id

    Doctor->>API: POST /consultations (record)
    API->>DB: insert consultation
    API->>DB: update appointment → completed

    Patient->>API: POST /monitoring/readings (vitals)
    API->>DB: insert health_reading
    API->>API: evaluate_severity()
    alt abnormal & not deduped
        API->>Redis: check + set dedup key
        API->>DB: insert alert
    end

    Doctor->>API: POST /ai/risk-assessment
    API->>DB: fetch recent readings
    API->>AI: predict(features)
    AI-->>API: risk_category, confidence
    API->>DB: insert prediction
    API-->>Doctor: risk assessment + recommendation

    Executive->>API: GET /dashboard/overview, /dashboard/trends
    API->>DB: aggregate patients, appointments,<br/>alerts, predictions
    API->>Redis: cache hot aggregates
    API-->>Executive: KPIs, trends, provider activity
```
