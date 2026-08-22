# Infra — Docker Compose

Local/full deployment profile (`docs/TRD.md` §2, `docs/architecture.md` §2).

## Quick start

```bash
cd infra
docker compose up -d --build
```

If `docker` isn't installed yet: `sudo apt install -y docker.io docker-compose-v2`, then
`sudo usermod -aG docker $USER && newgrp docker` (or open a new terminal) so you don't need
`sudo` for every `docker` command afterward. If a command in an *already-open* terminal still
says "permission denied... docker.sock", that terminal predates the group change — prefix with
`sudo` there, or open a new terminal.

- Backend (FastAPI): http://localhost:8000/docs
- Frontend (React/Vite): http://localhost:5173
- PostgreSQL: localhost:5432
- Redis: localhost:6379

Works out of the box with built-in defaults, including a default `JWT_SECRET_KEY` (see
`backend/app/core/config.py`). **Before any real/shared deployment**, copy
`../backend/.env.example` to `../backend/.env` (at minimum, set a real `JWT_SECRET_KEY`) and
`../frontend/.env.example` to `../frontend/.env`; `docker-compose.yml` can then be updated to
load them via `env_file`.

## Database setup (Phase 1) + dev login (Phase 2)

Once the stack is up, run these **inside the backend container** (not on the host — the host
doesn't have the Python deps installed, and `DATABASE_URL` resolves the `postgres` hostname
that only exists on the Docker network):

```bash
docker compose exec backend alembic upgrade head       # creates all 9 tables (docs/backend-schema.md)
docker compose exec backend python scripts/seed_dev_users.py   # admin@globalcare-demo.com / executive@... , password ChangeMe123!
docker compose exec backend python scripts/fetch_synthea.py    # downloads the Synthea CSV sample (~9 MB) into ../data (bind-mounted)
docker compose exec backend python scripts/seed_synthea.py --patients 200 --max-readings 5
```

Verified end-to-end against real PostgreSQL (2026-08-22, `docs/test-execution-log.md`): exactly
50 facilities/50 providers/200 patients/953 health_readings loaded, and `POST /auth/login`
returns a valid JWT.

`seed_dev_users.py` credentials are dev/demo only — never use them in a real deployment. See
`docs/backend-schema.md` §6 for the Synthea → schema field mapping, and `docs/api-spec.md` for
the full REST API contract (`/auth/*`, `/patients`, `/providers`, `/facilities`,
`/reports/registration` are implemented as of Phase 2).

## Services

| Service | Image/build | Purpose |
|---|---|---|
| `postgres` | `postgres:16-alpine` | System of record (`docs/backend-schema.md`) |
| `redis` | `redis:7-alpine` | Dashboard cache, alert de-dup, session/rate-limit (`deccission.md` ADR-002) |
| `backend` | `../backend/Dockerfile` | FastAPI app |
| `frontend` | `../frontend/Dockerfile` | React/Vite dev server |

Prometheus/Grafana/OPA services are added in Phase 7 (`docs/impmemnentaion-plan.md`).
