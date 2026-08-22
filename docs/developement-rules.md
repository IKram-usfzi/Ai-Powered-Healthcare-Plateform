# Development Rules & Conventions

**Related:** `impmemnentaion-plan.md`, `Testing-startegy.md`

## 1. Branching Strategy

- `main` — always deployable/demo-ready.
- `develop` — integration branch for in-progress work.
- `feature/<module>-<short-description>` — one branch per feature (e.g., `feature/monitoring-alerts`).
- `fix/<short-description>` — bug fixes.
- Merge to `develop` via pull request; merge `develop` → `main` at phase boundaries (see `impmemnentaion-plan.md`).

## 2. Commit Conventions

Conventional Commits style:

- `feat: add patient registration endpoint`
- `fix: correct abnormal-reading threshold for SpO2`
- `docs: update api-spec with monitoring endpoints`
- `chore: pin FastAPI dependency versions`
- `test: add unit tests for AI risk classifier`

## 3. Code Style

- **Python:** PEP 8; formatter/linter (e.g., Black + isort + Flake8/Ruff — tool choice confirmed at implementation start); type hints on public functions.
- **React/JS:** ESLint + Prettier; functional components; consistent naming matching the API resource names in `api-spec.md`.

## 4. Repository Structure (planned)

```
/backend        FastAPI application
/frontend       React application (per supplied UI/UX template)
/infra          Docker Compose files, AWS deployment configs
/docs           This documentation set + MkDocs site
/diagrams       Mermaid/PlantUML sources + exported diagrams
```

## 5. Environment & Secrets Management

- All secrets (DB credentials, JWT signing key, AWS keys) via environment variables, never committed.
- `.env.example` checked in with placeholder values; real `.env` files gitignored.
- AWS credentials scoped to least privilege needed for the free-tier deployment; never embedded in Docker images.

## 6. Pull Request / Review Checklist

- [ ] Linked to the relevant module/phase in `impmemnentaion-plan.md`
- [ ] Matches the contract in `api-spec.md` / schema in `backend-schema.md` (or updates them in the same PR)
- [ ] Tests added/updated per `Testing-startegy.md`
- [ ] No secrets committed
- [ ] Relevant `.md` docs updated if architecture/decisions changed (pair with a `deccission.md` entry if it's a real decision, not just a fix)

## 7. Dependency Management

- Python dependencies pinned (`requirements.txt` or `pyproject.toml` with locked versions).
- Node dependencies locked via `package-lock.json`.
- Trivy scan run against built images before considering a phase "done."

## 8. Definition of Done (per module)

A module is done when: its API endpoints match `api-spec.md`, its data model matches `backend-schema.md`, it has passing tests per `Testing-startegy.md`, it runs cleanly via `docker compose up`, and any resulting design decisions are logged in `deccission.md`.
