# Installation Guide

**Related:** `TRD.md` §8, `developement-rules.md`, `infra/docker-compose.yml`

Covers getting GlobalCare running locally via Docker Compose — the mandatory exam deliverable (`deccission.md` ADR-004). For the optional AWS profile, see `deployment-guide.md`.

## 1. Prerequisites

- Docker + Docker Compose v2 (`docker compose version`)
- 8–16 GB RAM, no GPU required (`TRD.md` §8)
- Git

Nothing else needs installing on the host — Python, Node, PostgreSQL, and Redis all run inside containers.

## 2. Clone the repository

```bash
git clone https://github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform.git
cd Ai-Powered-Healthcare-Plateform
```

## 3. Configure environment variables (optional for local dev)

`backend/.env.example` and `frontend/.env.example` document every variable `infra/docker-compose.yml` sets defaults for. For local development the committed defaults (`POSTGRES_USER=globalcare`, etc.) work out of the box — no `.env` file is required unless you want to override something (e.g. a real `JWT_SECRET_KEY` for anything beyond a throwaway demo).

## 4. Start the stack

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

This builds and starts all 7 services: `postgres`, `redis`, `opa`, `backend`, `frontend`, `prometheus`, `grafana`. First build takes a few minutes (installs Python/Node dependencies inside the images); subsequent starts are fast.

Check everything is healthy:

```bash
docker compose -f infra/docker-compose.yml ps
```

`postgres` and `redis` should show `(healthy)`; the rest show `Up`.

## 5. Run database migrations

```bash
docker compose -f infra/docker-compose.yml exec backend alembic upgrade head
```

## 6. Load demo data

```bash
# Two demo login accounts (administrator + executive), password ChangeMe123!
docker compose -f infra/docker-compose.yml exec backend python scripts/seed_dev_users.py

# Synthea-derived synthetic patients/providers/facilities/vitals
docker compose -f infra/docker-compose.yml exec backend python scripts/seed_synthea.py --patients 200 --max-readings 5
```

`seed_dev_users.py` creates `admin@globalcare-demo.com` and `executive@globalcare-demo.com` — see `user-guide.md` for what each role can do. `seed_synthea.py` populates ~200 patients, ~50 facilities/providers, and several hundred vitals readings so the dashboards have real data to show.

## 7. Verify

| Service | URL | Expected |
|---|---|---|
| Frontend | http://localhost:5173 | Login screen |
| Backend API docs | http://localhost:8000/docs | Swagger UI |
| Backend health | http://localhost:8000/api/v1/health | `{"status":"ok"}` |
| Prometheus | http://localhost:9090 | Targets page, `backend:8000` shows `UP` |
| Grafana | http://localhost:3001 | `admin`/`admin` — "GlobalCare API" dashboard |
| OPA | http://localhost:8181 | (no UI — policy API only) |

Log in at http://localhost:5173/login with `admin@globalcare-demo.com` / `ChangeMe123!` to confirm the full stack works end-to-end.

## 8. Run the test suite (optional, for developers)

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

77 tests should pass. See `Testing-startegy.md` and `test-execution-log.md` for the full test approach and history.

## Troubleshooting

- **A container is `Restarting` or `Exited`:** check its logs — `docker compose -f infra/docker-compose.yml logs <service>`. If `backend` is failing to boot, confirm `postgres`/`redis`/`opa` are healthy first (it depends on all three).
- **Frontend shows stale content after editing `tailwind.config.js`/`postcss.config.js`/`eslint.config.js`:** these are bind-mounted (`deccission.md` ADR-023) but only picked up on container *recreate*, not a plain restart — run `docker compose -f infra/docker-compose.yml up -d --no-deps frontend`.
- **Ports already in use:** another process (or a leftover container from a previous run) may be holding 5173/8000/5432/6379/8181/9090/3001. `docker compose -f infra/docker-compose.yml down` and retry, or check `docker ps` / `lsof -i :<port>`.
