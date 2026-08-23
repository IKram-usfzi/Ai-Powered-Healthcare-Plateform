# 5. Remote Patient Monitoring Architecture Diagram

**Source:** `docs/flow.md` §3 (Remote Monitoring & Alert Flow), `app/services/vitals.py`, `app/core/redis_client.py`.

```mermaid
flowchart TB
    PAT["Patient<br/>(self-submission)"] -->|"POST /monitoring/readings"| INGEST

    subgraph API["FastAPI — Monitoring API"]
        INGEST["Ingestion endpoint"]
        THRESH["Threshold check<br/>(app/services/vitals.py —<br/>3 severity tiers × 5 vitals)"]
        DEDUP{"Redis dedup key<br/>exists for this patient<br/>in the last 5 min?"}
        ALERTAPI["GET /monitoring/alerts<br/>PATCH .../acknowledge"]
    end

    INGEST --> PG[("PostgreSQL<br/>health_readings")]
    INGEST --> THRESH
    THRESH -->|"normal"| DONE["stored only, no alert"]
    THRESH -->|"abnormal"| DEDUP
    DEDUP -->|"yes — suppress"| DONE
    DEDUP -->|"no — create alert"| ALERT[("PostgreSQL<br/>alerts")]
    DEDUP -->|"set key, 5 min TTL"| REDIS[("Redis")]

    DOC["Doctor"] -->|"view/acknowledge"| ALERTAPI
    ADM["Administrator"] -->|"view"| ALERTAPI
    ALERTAPI --> ALERT
```

Exit criteria (Phase 4): a simulated abnormal reading correctly produces exactly one alert — verified against real Redis, not just the test fake (`docs/test-execution-log.md` Phase 4).
