# Testing Strategy

**Related:** `impmemnentaion-plan.md`, `api-spec.md`, `Security.md`

## 1. Objectives

Demonstrate that each module works correctly, that the AI model's performance is measurable and explainable, and that the security posture holds up — producing the "test reports," "AI evaluation report," and "security scan report" GitHub deliverables (brief §11).

## 2. Test Levels

| Level | Scope | Planned tooling |
|---|---|---|
| Unit | Business logic, AI preprocessing/inference functions | pytest |
| Integration | API ↔ PostgreSQL ↔ Redis interactions | pytest + test containers/test DB |
| API | Endpoint contracts vs. `api-spec.md` | pytest + FastAPI TestClient, or Postman/Newman |
| Frontend | Component/interaction tests | React Testing Library |
| End-to-end | Full user journeys per persona (registration → appointment → monitoring → AI → dashboard) | Manual scripted run-through for the demo; light E2E automation if time allows |
| Security | Image/dependency vulnerabilities | Trivy |

## 3. AI Model Evaluation

- Train/test split on the Synthea-derived synthetic dataset.
- Metrics: accuracy, precision, recall, F1-score, confusion matrix per risk category.
- Confidence scores reported alongside predictions (per Module 4 requirement).
- Evaluation results compiled into the "AI evaluation report" deliverable, explicitly framed around decision-support (not diagnostic) performance, per NIST AI RMF-style transparency (see `Security.md` §10).

## 4. Test Data Strategy

- All test data is synthetic (Synthea-derived; optionally supplemented per `deccission.md` ADR-011).
- Tests run against an isolated test database/schema, never against demo or "production-like" data used for the live viva demo.

## 5. Test Environment

A dedicated Docker Compose test profile (or test-specific service overrides) so tests don't interfere with the state used for the live demonstration.

## 6. Coverage Targets (qualitative)

- Every mandatory functional capability listed per module in `PRD.md` §6 has at least one passing happy-path test.
- Key edge cases: abnormal vitals thresholds (Module 3), low-confidence AI predictions (Module 4), and role-based access denial (Security) are explicitly covered.
- 100% line coverage is not a goal for this POC; correctness of the demoed capabilities is.

## 7. Test Execution Summary

A running log/report of test runs (pass/fail counts, notable failures and fixes) maintained as implementation proceeds, to satisfy the "test execution summary" requirement in the live demonstration stage (brief §10, Stage 2).

## 8. Regression Discipline

Any change to `api-spec.md` or `backend-schema.md` triggers a review of related tests before merge (see `developement-rules.md` §6 PR checklist).
