# Presentation Outline (15–20 minutes)

**Related:** `PRD.md`, `demo-script.md`, `viva-prep.md`

A talk track for the exam's presentation stage. Timings are guides, not a script to read verbatim — know the material well enough to speak from bullet points and adjust pace live.

## 1. Problem & context (2 min)

- GlobalCare Telehealth Network: nationwide digital healthcare platform, 8M+ simulated patients (`PRD.md` §2).
- **The problem:** registration, scheduling, telemedicine, and monitoring live in separate systems. Clinicians have no unified view of a patient across appointments, monitoring, and AI assessment; alerts are inconsistent; no operational analytics (`PRD.md` §3).
- **The goal:** one platform, five modules, real proof-of-concept — not slideware.

## 2. Solution overview (3 min)

- Five modules: Patient/Provider Management, Telemedicine, Remote Patient Monitoring, AI Health Risk Assessment, Executive Dashboard (`PRD.md` §6).
- One React frontend, one FastAPI backend, PostgreSQL system of record, Redis for cache/de-dup, a real trained AI model.
- Show diagram 1 or 2 from `docs/diagrams/` (Enterprise Architecture / High-Level Solution Architecture) — this is the single slide that orients the whole talk.

## 3. Architecture & technology choices (3 min)

- Docker Compose is the mandatory deployment profile; everything runs on an 8–16 GB laptop, no GPU (`TRD.md` §8).
- Why these choices, not others — pick 2–3 ADRs that invite good questions: OPA over hand-rolled RBAC (ADR-006/024), Redis scoped narrowly rather than a general cache (ADR-002), Synthea over fabricated data (ADR-005/017).
- Security and observability as cross-cutting, not bolted on: JWT + OPA (real policy decisions, fail-closed), Prometheus/Grafana live metrics, Trivy scanning.

## 4. What's real, not simulated (2 min)

This is the differentiator worth stating explicitly — anticipate "how much of this is actually working vs. mocked":

- Every number in every dashboard is a real SQL aggregation — no fabricated KPIs (ADR-022).
- The AI model is genuinely trained (RandomForestClassifier, 957 real readings) with real measured accuracy/precision/recall, documented honestly including its weak points (`ai-evaluation-report.md`'s thin `high`-risk class).
- OPA is a real running policy engine making real allow/deny decisions over HTTP, not a stub.
- 77 automated tests + verification against real Docker Compose infrastructure for every phase (`test-execution-log.md`).

## 5. Live demo (5–10 min)

Hand off to `demo-script.md` — don't narrate the demo here, just set it up: "I'll now show this running live, not slides."

## 6. Engineering rigor & real bugs found (2 min)

Pick 1–2 concrete examples — these demonstrate genuine engineering practice better than any slide:

- The Docker `WORKDIR` path bug pattern (`SYNTHEA_DATA_DIR`/`DOCS_DIR`) — found by *running* the container, not by reading the code, recurred and was recognized the second time.
- The Trivy scan finding two real CVEs (`python-jose`, `python-multipart`) in directly-pinned dependencies, fixed and re-verified.
- Optional: the environment-recovery incident (a wiped sandbox, recovered from GitHub with zero data loss) — shows resilience, not just happy-path competence.

## 7. Scope & honesty about limits (2 min)

- Docker Compose is mandatory and done; AWS (Phase 8) is real Terraform, validated, deliberately **not deployed** — explain why (cost, scope discipline) rather than let it look unfinished.
- The brief only mandates the Dashboard for the frontend — the Patients/Appointments/Telemedicine/Monitoring/Analytics screens (`UIUX.md` §6, ADR-029) were built afterward as a deliberate scope expansion, not required. Worth naming as evidence of going beyond the minimum, not as a gap to explain away.
- AI output is explicitly decision-support only, never framed as diagnosis (`PRD.md` §7) — a deliberate constraint, not a gap.

## 8. Close (1 min)

- Recap: 5 modules, real data, real tests, real infra verification, full documentation set including all 17 mandatory diagrams.
- Invite questions — transition into the viva.
