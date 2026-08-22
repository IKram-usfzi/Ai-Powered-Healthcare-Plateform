# Infra — Docker Compose

Local/full deployment profile (`docs/TRD.md` §2, `docs/architecture.md` §2).

## Quick start

```bash
cd infra
docker compose up --build
```

- Backend (FastAPI): http://localhost:8000/docs
- Frontend (React/Vite): http://localhost:5173
- PostgreSQL: localhost:5432
- Redis: localhost:6379

Works out of the box with built-in defaults — no `.env` file required for this Phase 0
scaffold. Before real credentials/secrets exist (Phase 2+), copy `../backend/.env.example`
to `../backend/.env` and `../frontend/.env.example` to `../frontend/.env` and adjust values;
`docker-compose.yml` can then be updated to load them via `env_file`.

## Services

| Service | Image/build | Purpose |
|---|---|---|
| `postgres` | `postgres:16-alpine` | System of record (`docs/backend-schema.md`) |
| `redis` | `redis:7-alpine` | Dashboard cache, alert de-dup, session/rate-limit (`deccission.md` ADR-002) |
| `backend` | `../backend/Dockerfile` | FastAPI app |
| `frontend` | `../frontend/Dockerfile` | React/Vite dev server |

Prometheus/Grafana/OPA services are added in Phase 7 (`docs/impmemnentaion-plan.md`).
