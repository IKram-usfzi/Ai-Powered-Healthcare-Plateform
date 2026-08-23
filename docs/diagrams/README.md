# Diagrams

All 17 mandatory diagrams (`docs/architecture.md` §6, exam brief §8), as real Mermaid
diagrams-as-code — diffable in Git, rendered natively by the MkDocs Material theme
(`pymdownx.superfences` custom fence config in `mkdocs.yml`), and by GitHub's own
Markdown renderer.

| # | File | Source |
|---|---|---|
| 1 | [`01-enterprise-architecture.md`](01-enterprise-architecture.md) | `PRD.md` §1–2, `architecture.md` §1 |
| 2 | [`02-high-level-solution-architecture.md`](02-high-level-solution-architecture.md) | `architecture.md` §2 |
| 3 | [`03-detailed-system-architecture.md`](03-detailed-system-architecture.md) | `architecture.md` §3–4 |
| 4 | [`04-telemedicine-architecture.md`](04-telemedicine-architecture.md) | `flow.md` §2 |
| 5 | [`05-remote-monitoring-architecture.md`](05-remote-monitoring-architecture.md) | `flow.md` §3 |
| 6 | [`06-ai-risk-assessment-architecture.md`](06-ai-risk-assessment-architecture.md) | `flow.md` §4 |
| 7 | [`07-clinical-workflow-architecture.md`](07-clinical-workflow-architecture.md) | `flow.md` (all) |
| 8 | [`08-enterprise-network-architecture.md`](08-enterprise-network-architecture.md) | `architecture.md` §5, `infra/terraform/` |
| 9 | [`09-network-flow.md`](09-network-flow.md) | `infra/docker-compose.yml`, `infra/terraform/` |
| 10 | [`10-data-flow-level-0.md`](10-data-flow-level-0.md) | `api-spec.md` |
| 11 | [`11-data-flow-level-1.md`](11-data-flow-level-1.md) | `backend-schema.md` |
| 12 | [`12-telemedicine-workflow.md`](12-telemedicine-workflow.md) | `flow.md` §2 |
| 13 | [`13-remote-monitoring-workflow.md`](13-remote-monitoring-workflow.md) | `flow.md` §3 |
| 14 | [`14-ai-prediction-workflow.md`](14-ai-prediction-workflow.md) | `flow.md` §4 |
| 15 | [`15-healthcare-operations-workflow.md`](15-healthcare-operations-workflow.md) | `flow.md` §5, `UIUX.md` §3 |
| 16 | [`16-database-erd.md`](16-database-erd.md) | `backend-schema.md` §1–2, real SQLAlchemy models |
| 17 | [`17-end-to-end-sequence.md`](17-end-to-end-sequence.md) | `flow.md` §6 |

Draw.io is reserved for presentation-specific layout needs (ADR-008) — not used here;
every diagram matches the real, implemented system (Phases 0–8), not just the original
design-time sketches in `docs/`.
