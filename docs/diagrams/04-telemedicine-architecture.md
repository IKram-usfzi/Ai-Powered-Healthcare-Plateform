# 4. Telemedicine Platform Architecture Diagram

**Source:** `docs/flow.md` §2 (Telemedicine Appointment & Consultation Flow).

```mermaid
flowchart TB
    PAT["Patient"] -->|"book appointment"| API
    ADM["Administrator"] -->|"book on behalf of patient"| API

    subgraph API["FastAPI — Telemedicine API"]
        BOOK["POST /appointments"]
        STATUS["PATCH /appointments/{id}/status"]
        CONSULT["POST /consultations<br/>(auto-completes appointment)"]
        SCHED["GET /providers/{id}/schedule"]
        HIST["GET /consultations/{patientId}"]
        RPT["GET /reports/appointments"]
    end

    DOC["Doctor"] -->|"view schedule"| SCHED
    DOC -->|"update status"| STATUS
    DOC -->|"record consultation summary"| CONSULT

    BOOK --> PG[("PostgreSQL<br/>appointments")]
    STATUS --> PG
    CONSULT --> PGC[("PostgreSQL<br/>consultations")]
    CONSULT -->|"status → completed"| PG
    SCHED --> PG
    HIST --> PGC
    RPT --> PG

    PAT -->|"view own history"| HIST
    DOC -->|"view own patients' history"| HIST
    ADM -->|"operational report"| RPT
```

Role scoping: a doctor only sees/acts on their own appointments and schedule; consultation history is additionally restricted to the doctor's own appointments with that patient — an extension of the assigned-patient rule (`Security.md` §3) to the appointment relationship.
