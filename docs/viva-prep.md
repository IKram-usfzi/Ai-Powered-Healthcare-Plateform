# Viva Voce Prep (30–40 minutes)

**Related:** `deccission.md` (every answer below should trace back to a real ADR), `presentation-outline.md`, `demo-script.md`

Two parts: general defense-of-decisions questions (Part A), and the five named scenario-based redesign questions (Part B). Prepare to justify every answer by pointing at a specific ADR, file, or measured result — "because I decided to" is weak; "because ADR-006 scoped OPA narrowly to avoid building a general policy platform we didn't need" is strong.

## Part A — Likely general questions

**"Why FastAPI over Django/Flask/Express?"**
ADR-001. Async-native, automatic OpenAPI/Swagger docs (used live in the demo), Pydantic validation built in — matched the "REST API + role-based access + fast iteration" shape of the brief better than a batteries-included framework the project didn't need the batteries of.

**"Why is OPA only enforcing role checks, not the row-level 'doctor's own patients' rule?"**
ADR-024. Security.md §9's own threat table already assigns row-level checks to the API layer, not OPA. Rewriting ~8 existing, tested call sites into per-request OPA calls was real, avoidable risk for a rule OPA doesn't need to own — the row-level Rego policy (`allow_patient_access`) is authored and unit-tested (11/11 `opa test`) to prove the pattern, just not wired in. Know this cold — it's the single most likely "why didn't you do X properly" question.

**"How do you know OPA is actually being used, not just decorative?"**
`require_roles()` calls a real OPA server over HTTP and fails closed on any error (`app/core/opa_client.py`). Demonstrated live: real 403 for a role OPA denies, real 200 for one it allows, verified via direct `curl` to `:8181/v1/data/...` during Phase 7 (`test-execution-log.md`). Also: a real production incident this session — OPA's bind mount detached after an environment reset, and every request failed closed with 403 until fixed, which is exactly the fail-closed behavior working, just against an infra problem.

**"Why Redis, and why so narrowly scoped?"**
ADR-002. De-dup (5-min per-patient key stops alert spam), dashboard cache, session/rate-limit — not a general-purpose cache reached for by default. Redis sat unused in Docker Compose from Phase 0 until Phase 4 actually needed it.

**"Is the AI model any good? Be honest."**
Show `ai-evaluation-report.md` directly. Accuracy 0.995 is misleading on its own (label imbalance — `low` dominates); macro precision/recall are ~0.64–0.67 and the `high`-risk class has only 3 examples in test, reported transparently rather than hidden. This is the correct answer to give, not a defensive one — the honesty about the weak class is itself evidence of engineering maturity, not a flaw to minimize.

**"What happens if the AI is wrong?"**
It's explicitly framed as decision-support, never diagnosis — every response includes a recommendation stating clinical judgement is required (`PRD.md` §7). No auto-actioning on AI output anywhere in the system.

**"Why isn't this deployed to AWS if the Terraform exists?"**
ADR-027, deliberate scope decision this session: Docker Compose is the mandatory profile (ADR-004); AWS costs real money and needs babysitting/teardown discipline for a capstone with no ongoing owner. The Terraform is real and `validate`-clean, ready when actually wanted — not deployed is a choice, not a gap.

**"What's your test coverage story?"**
77 automated pytest tests + 11 Rego policy tests, but the more important claim: every implementation phase (2 through 7) was also verified against real Docker Compose infrastructure — real PostgreSQL, real Redis, real OPA — not just mocks. `test-execution-log.md`'s "At a glance" table has the phase-by-phase breakdown.

**"What would you do differently with more time?"**
Good honest answers: dedicated management UIs beyond the dashboard (patient list, appointment booking screens) — the brief only mandates the dashboard for frontend, so this was correctly out of scope, not forgotten; wiring the row-level OPA policy into the API layer if row-level authorization complexity grows; a CI pipeline running the test suite + Trivy scan on every push (currently run manually per-phase).

## Part B — Scenario-based redesign questions

For each: what changes, what stays, and why — anchor answers in the existing architecture's actual extension points, not hand-waving.

### 1. National telemedicine network (much larger scale, e.g. 8M+ real patients)

- **Stays:** the module boundaries (Patient/Provider, Telemedicine, Monitoring, AI, Dashboard) — they're already independently scalable REST APIs behind one gateway, not a monolith with hidden coupling.
- **Changes:** PostgreSQL would need read replicas / partitioning by region or facility; Redis would need to move from a single instance to a cluster; the stateless JWT design (ADR: no server-side session) already supports horizontal API scaling without rework. The AI service would likely move from in-process inference to a dedicated model-serving layer (batch or async) to avoid blocking API latency at scale. OPA's narrow policy set stays narrow, but its data source would need to move from static Rego to bundle-based policy distribution for a multi-region deployment.

### 2. Rural healthcare (low bandwidth, intermittent connectivity)

- **Changes:** the React frontend would need offline-first patterns (local caching, queued writes) — not present today, since the exam brief assumes a connected demo environment. Remote monitoring ingestion (`/monitoring/readings`) would benefit from batched/store-and-forward submission rather than one-request-per-reading. The AI risk assessment could run periodically in batch rather than on-demand, tolerating connectivity gaps.
- **Stays:** the core data model and alert de-dup logic are connectivity-agnostic — Redis's 5-minute dedup window would just need to account for delayed/batched submissions rather than assuming near-real-time delivery.

### 3. Disaster response (surge load, rapid triage priority)

- **Changes:** the alert severity model (`app/services/vitals.py`) would need a triage-priority dimension layered on top of clinical severity — right now severity reflects vitals abnormality, not response urgency under surge conditions. The Executive Dashboard's aggregate queries would need to support real-time surge visualizations (patients-per-hour, capacity vs. load) rather than the current daily/weekly aggregates.
- **Stays:** the alert de-dup and role-scoped access pattern (doctor sees only relevant patients) actually matters *more* under surge — it's already designed to prevent alert fatigue, which is exactly the failure mode disaster response can't afford.

### 4. Elderly care (chronic monitoring, caregiver involvement)

- **Changes:** the role model (Patient/Doctor/Administrator/Executive) has no "Caregiver" or "Family Member" role today — would need a new role with read-only, consent-scoped access to a specific patient's data, extending the existing OPA/API-layer authorization pattern rather than replacing it. Remote monitoring would benefit from longer-baseline trend analysis (weeks/months) rather than the current 5-vitals-per-reading snapshot model, to catch gradual decline, not just acute abnormal readings.
- **Stays:** the assigned-provider relationship and row-level authorization are the right foundation for adding a caregiver role — it's an additive role, not an architectural change.

### 5. International programmes (multi-language, multi-jurisdiction compliance)

- **Changes:** the frontend has no i18n today (`UIUX.md` doesn't address it) — would need a translation layer, likely react-i18next, and RTL layout support depending on target languages. Compliance is bigger: `Security.md` §10's conceptual alignment (HIPAA/GDPR "conceptual only, no real PHI") would need to become real region-specific compliance work — data residency (which PostgreSQL instance, which region), consent management, and potentially per-jurisdiction OPA policies (the narrow-policy-set pattern extends naturally to jurisdiction-specific rules).
- **Stays:** the FHIR-inspired schema design (ADR-003) was chosen partly *because* it's a recognized international interoperability standard — that decision pays off directly in a multi-jurisdiction scenario, since it's not a US-specific or region-specific data model.

## General framing for all five

The honest, confident answer pattern: "the module boundaries and the security/data model were designed narrowly and deliberately for this brief, but the extension points are real — [specific mechanism] is where this scenario's requirement would attach, without a rewrite of [specific thing that stays]." Never claim the current system already handles a scenario it doesn't — the examiners are testing whether you understand the difference between what's built and what a real redesign would require.
