# 13. Remote Monitoring Workflow Diagram

**Source:** `docs/flow.md` §3, `backend/tests/test_monitoring.py::test_abnormal_reading_produces_exactly_one_alert_deduped` (the literal Phase 4 exit criteria, verified against real Redis).

```mermaid
sequenceDiagram
    actor Patient
    actor Doctor
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Redis

    Patient->>API: POST /monitoring/readings (reading 1, abnormal)
    API->>DB: insert health_reading
    API->>API: evaluate_severity() → abnormal
    API->>Redis: dedup key exists?
    Redis-->>API: no
    API->>DB: insert alert
    API->>Redis: set dedup key (5 min TTL)
    API-->>Patient: reading recorded, alert raised

    Patient->>API: POST /monitoring/readings (reading 2, abnormal)
    API->>DB: insert health_reading
    API->>API: evaluate_severity() → abnormal
    API->>Redis: dedup key exists?
    Redis-->>API: yes — suppress
    API-->>Patient: reading recorded, no new alert

    Patient->>API: POST /monitoring/readings (reading 3, abnormal)
    API->>DB: insert health_reading
    API->>Redis: dedup key exists?
    Redis-->>API: yes — suppress
    API-->>Patient: reading recorded, no new alert

    Doctor->>API: GET /monitoring/alerts
    API->>DB: query alerts (assigned patients only)
    DB-->>API: exactly 1 alert
    API-->>Doctor: 1 alert (severity: critical)

    Doctor->>API: PATCH /monitoring/alerts/{id}/acknowledge
    API->>DB: update alert status
    API-->>Doctor: acknowledged
```
