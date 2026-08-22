# Security Design & Compliance Mapping

**Related:** `TRD.md`, `api-spec.md`, `deccission.md` (ADR-006, ADR-009)

## 1. Objectives

Protect simulated patient data with production-representative controls, demonstrate DevSecOps practice, and show conceptual alignment with recognized healthcare/security standards — without claiming certified compliance.

## 2. Authentication

JWT-based authentication via FastAPI. Tokens carry role claims (`patient`, `doctor`, `administrator`, `executive`). Access tokens short-lived; refresh flow via `/auth/refresh` (see `api-spec.md`).

## 3. Authorization

Role-based access control enforced through a narrow, explicit set of OPA (Open Policy Agent) Rego policies — e.g., "a doctor may read/write only their assigned patients' records," "an executive may read aggregate data but not individual patient records," "an administrator has full CRUD over registration data." Scope intentionally kept small (ADR-006) rather than building a general policy platform.

## 4. Data Protection

- All data is synthetic; still handled as if sensitive, to model real-world practice.
- Transport encryption: HTTPS/TLS for all API traffic (including the AWS deployment, via the load balancer/CloudFront layer or a TLS-terminating reverse proxy).
- At-rest protection: relies on the underlying platform (RDS encryption at rest for the AWS profile; local Docker volume for the laptop profile — noted as a scope limitation for the POC).

## 5. Secrets Management

No secrets committed to Git. Environment variables for DB credentials, JWT signing key, and AWS credentials; `.env.example` checked in with placeholders only (see `developement-rules.md` §5).

## 6. Vulnerability Scanning

Trivy scans built Docker images (and optionally filesystem/dependencies) before/at deployment. Output captured as the "security scan report" GitHub deliverable (brief §11).

## 7. Network Security (AWS profile)

VPC with public subnet (EC2 app tier) and private subnet (RDS). Security groups restrict inbound traffic to required ports (22 for admin SSH, 80/443 for the app). Database not directly internet-reachable.

## 8. Audit Logging

Key actions (registration, role-based data access, AI predictions, alert acknowledgement) logged with actor, timestamp, and action type — supports both operational traceability and the "AI governance" viva topic (brief §10, Stage 3).

## 9. Threat Model Summary (lightweight)

| Threat | Mitigation |
|---|---|
| Unauthorized data access | JWT + OPA RBAC |
| Credential leakage | No secrets in repo; short-lived tokens |
| Vulnerable dependencies/images | Trivy scanning |
| Cross-role data leakage (e.g., patient viewing another patient's data) | Row-level authorization checks tied to JWT identity, enforced at the API layer |
| Unrestricted network exposure (AWS) | VPC segmentation, security groups, DB in private subnet |

## 10. Standards & Frameworks — Conceptual Alignment

| Standard | How this project addresses it (conceptually) |
|---|---|
| HL7 FHIR | FHIR-inspired resource schemas (Patient, Observation, Encounter) — ADR-003 |
| DICOM | Not implemented; noted as out of scope for this POC |
| ISO 13131 (Telehealth) | Telemedicine module designed around scheduling/consultation/status-tracking best practice |
| ISO 15189 / ISO 13485 | Conceptual awareness only; no lab/device certification claimed |
| ISO/IEC 27001 | Security controls (auth, RBAC, scanning, secrets mgmt) modeled on ISMS practice |
| ISO/IEC 27701 | Data minimization (synthetic-only data), access control mapped to privacy principles |
| ISO/IEC 42001 (AI Management) | AI predictions logged, versioned, and framed as decision-support with mandatory human review |
| NIST AI RMF | Model evaluation, confidence scoring, and human-in-the-loop framing (see `Testing-startegy.md` §3) |
| NIST CSF 2.0 | Identify/Protect/Detect functions reflected via inventoried assets, RBAC, monitoring, and alerting |
| HIPAA | Conceptual only — no real PHI is processed, so certified compliance is not claimed |
| GDPR | Conceptual only — synthetic data avoids real personal-data obligations |
| OWASP Top 10 | Addressed via input validation (Pydantic), auth, dependency scanning, and secure defaults |
| CIS Critical Security Controls | Reflected in secrets management, scanning, and network segmentation practices |

## 11. Incident Response (POC scope)

Formal incident response is out of scope for a capstone proof-of-concept; the audit log (§8) and alerting (§9) provide the traceability that a real incident-response process would build on.
