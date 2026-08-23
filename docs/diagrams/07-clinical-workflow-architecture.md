# 7. Clinical Workflow Architecture Diagram

**Source:** `docs/flow.md` (all sections) — the clinical journey across all five modules at an architecture level, distinct from the detailed end-to-end sequence diagram (§17).

```mermaid
flowchart LR
    START(["Patient registered"]) --> APPT["Appointment scheduled<br/>& consultation recorded<br/>(Module 2)"]
    APPT --> MON["Vitals submitted &<br/>continuously monitored<br/>(Module 3)"]
    MON -->|"abnormal reading"| ALERT["Alert raised,<br/>de-duplicated, acknowledged<br/>by clinician"]
    MON --> AI["Doctor requests<br/>AI risk assessment<br/>(Module 4)"]
    ALERT --> AI
    AI --> REVIEW["Clinical judgement:<br/>doctor reviews AI output,<br/>decides on care plan"]
    REVIEW --> APPT
    REVIEW --> DASH["Aggregated into<br/>Executive Dashboard<br/>(Module 5)"]
    APPT --> DASH
    MON --> DASH
    ALERT --> DASH

    DASH --> DECIDE["Executive/Administrator<br/>operational decisions:<br/>staffing, resourcing,<br/>risk-flagged follow-up"]
```

Continuity of care is the design goal this diagram illustrates: a patient's record stays consistent across scheduling, monitoring, and AI assessment rather than fragmenting across separate systems (`docs/flow.md` §1), and every clinical/operational signal ultimately surfaces on the dashboard that executives and administrators use to act on it.
