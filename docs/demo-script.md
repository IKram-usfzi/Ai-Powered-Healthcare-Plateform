# Live Demo Script (5–10 minutes)

**Related:** `presentation-outline.md`, `installation-guide.md`, `user-guide.md`

A precise walkthrough to rehearse until it's fast and reliable. Practice this exact sequence more than once — a live demo that stalls looking for a button costs more credibility than a shorter, confident one.

## Before you start (do this the night before, not 5 minutes before)

```bash
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps   # all 7 should be Up/healthy
curl -s http://localhost:8181/v1/policies        # must NOT be [] — see installation-guide.md
                                                  # troubleshooting if it is
```

Have three browser tabs ready: `http://localhost:5173` (app), `http://localhost:8000/docs` (Swagger), `http://localhost:3001` (Grafana). Know the demo credentials cold: `admin@globalcare-demo.com` / `executive@globalcare-demo.com`, both `ChangeMe123!`.

## 1. Login and role-based routing (1 min)

- Open `http://localhost:5173/login`.
- Log in as `executive@globalcare-demo.com`. **Say out loud:** "Notice it redirected me straight to the Executive Overview — that's role-based routing, not a manual choice."
- Point at the KPI cards: Total Patients, Active Providers, Open Alerts, AI Risk Alerts. **Say:** "Every one of these is a live SQL query against PostgreSQL, not a hard-coded number."

## 2. Executive Dashboard depth (1–2 min)

- Point at the Chart.js trend line — 7 days of vitals readings vs. clinical alerts.
- Scroll to the AI Risk Assessment panel and the Operational Efficiency section (Scheduled/Completed/Cancelled).
- Click **Export Data** — a real JSON file downloads. Open it briefly to show it's the full aggregated report, not a canned export.

## 3. Role enforcement, live (1 min)

- Log out, log in as `admin@globalcare-demo.com`.
- Try navigating directly to `http://localhost:5173/dashboard/executive`. **Say:** "Administrator isn't Executive — watch it redirect back." This demonstrates `ProtectedRoute` *and* the underlying OPA-backed API rejection, not just a UI-level restriction.
- Optional, if time allows: open Swagger (`:8000/docs`), call `POST /patients` with the admin's token and no `Authorization` header — show the `403` — then with the header — show it succeeds.

## 4. Healthcare Operations view (1 min)

- Navigate to `/dashboard/operations` (or click the "Operations" pill).
- Point at "Busiest Providers Today" (real per-provider appointment counts) and the alerts panel. **Say:** "Where the supplied template assumed data we don't track — bed occupancy, no-shows — we substituted the closest real equivalent instead of inventing a number."

## 5. AI Risk Assessment via API (1–2 min)

- Switch to Swagger (`:8000/docs`).
- `POST /api/v1/ai/risk-assessment` with a real patient ID from the seeded data (any assigned patient) as a doctor-role token, or narrate the response shape from a pre-run example if getting a doctor token live is too slow.
- **Say:** "This is a real trained RandomForestClassifier — 957 real readings, measured accuracy shown in `docs/ai-evaluation-report.md` — and the recommendation text always states this requires clinical judgement, never a diagnosis."

## 6. Observability, live (1 min)

- Switch to Grafana (`:3001`, `admin`/`admin`).
- Open the "GlobalCare API" dashboard. **Say:** "This is scraping real Prometheus metrics off the backend right now" — refresh the page or trigger a couple of requests in another tab to show the numbers move.

## 7. Wrap (30 sec)

- **Say:** "Everything you just saw — the dashboards, the AI prediction, the role enforcement, the metrics — is real infrastructure, verified end-to-end, not a mock." Transition back to the presenter or into Q&A.

## If something breaks mid-demo

- Blank dashboard / everything 403s → OPA lost its policies (see `installation-guide.md` troubleshooting) — `docker compose -f infra/docker-compose.yml up -d --force-recreate --no-deps opa`, refresh.
- A container is down → `docker compose -f infra/docker-compose.yml ps`, then `logs <service>`.
- Don't debug live for more than ~30 seconds — narrate what *should* happen from `docs/` and move on; a calm recovery reads better than a long silent pause.
