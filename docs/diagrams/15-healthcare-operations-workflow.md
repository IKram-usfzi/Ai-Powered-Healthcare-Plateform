# 15. Healthcare Operations Workflow Diagram

**Source:** `docs/flow.md` §5, `docs/UIUX.md` §3 (3-view dashboard), `backend/app/api/v1/dashboard.py` — reflects the real Phase 6 implementation.

```mermaid
sequenceDiagram
    actor User as Administrator / Executive
    participant FE as React Frontend
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Redis

    User->>FE: log in
    FE->>API: POST /auth/login
    API-->>FE: JWT (role claim)
    FE->>FE: redirect by role<br/>(executive → /dashboard/executive,<br/>else → /dashboard)

    FE->>API: GET /dashboard/overview
    API->>DB: aggregate patients, appointments,<br/>monitoring, alerts, predictions
    API-->>FE: DashboardOverview (real counts, no fabricated KPIs)

    alt Executive on /dashboard/executive
        FE->>API: GET /dashboard/trends
        API->>DB: 7-day vitals/alerts aggregation
        API-->>FE: DashboardTrends
        FE->>FE: render Chart.js trend line
        User->>FE: click "Export Data"
        FE->>API: GET /reports/executive
        API->>API: build_overview + build_trends +<br/>build_provider_activity
        API-->>FE: ExecutiveReport (JSON)
        FE->>User: download JSON file
    else Administrator on /dashboard/operations
        FE->>API: GET /dashboard/provider-activity
        API->>DB: per-provider appointment/patient counts
        API-->>FE: busiest-providers table
        FE->>API: GET /monitoring/alerts
        API-->>FE: alerts (or 403 if role not Doctor/Admin)
    end
```

Wherever the supplied template assumed untracked data (bed occupancy, no-show rate, provider presence), the real implementation substitutes a computable equivalent instead of fabricating a number — `deccission.md` ADR-022.
