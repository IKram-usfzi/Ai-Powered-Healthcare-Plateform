# Infra

`docker-compose.yml` is the mandatory local deployment profile (`docs/TRD.md` §8, `deccission.md` ADR-004) — 7 services: `postgres`, `redis`, `opa`, `backend`, `frontend`, `prometheus`, `grafana`. `docker-compose.aws.yml` is a companion override for the optional AWS profile (`terraform/`, not deployed — ADR-027).

Full setup, verification, and troubleshooting steps: [`../docs/installation-guide.md`](../docs/installation-guide.md).
Deployment profile comparison (local vs. AWS): [`../docs/deployment-guide.md`](../docs/deployment-guide.md).
AWS Terraform module: [`terraform/README.md`](./terraform/README.md).

## Quick reference

```bash
docker compose -f docker-compose.yml up -d --build      # from the repo root
docker compose -f docker-compose.yml ps                 # check health
docker compose -f docker-compose.yml logs <service>      # debug a specific container
```

| Service | Port | Purpose |
|---|---|---|
| `postgres` | 5432 | System of record (`docs/backend-schema.md`) |
| `redis` | 6379 | Dashboard cache, alert de-dup, session/rate-limit (ADR-002) |
| `opa` | 8181 | RBAC policy decisions (`opa/policies/`, ADR-006/ADR-024) |
| `backend` | 8000 | FastAPI app — all 5 modules' APIs + `/metrics` |
| `frontend` | 5173 | React/Vite dev server — JWT login + 3-view dashboard |
| `prometheus` | 9090 | Scrapes `backend:8000/metrics` |
| `grafana` | 3001 | `admin`/`admin` — provisioned "GlobalCare API" dashboard |
