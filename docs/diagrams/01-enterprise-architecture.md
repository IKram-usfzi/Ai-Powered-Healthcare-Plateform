# 1. Enterprise Digital Healthcare Architecture Diagram

**Source:** `docs/PRD.md` §1–2 (GlobalCare Telehealth Network context, 8M+ simulated patients), `docs/architecture.md` §1.

The big-picture view: GlobalCare's four user personas, the five product modules they use, the platform layer underneath, and the cross-cutting concerns (security, observability) and standards this project conceptually aligns with — not a network or deployment diagram, those are separate (§8, §9).

```mermaid
flowchart TB
    subgraph USERS["GlobalCare Telehealth Network — Users"]
        PAT["Patient"]
        DOC["Doctor / Provider"]
        ADM["Administrator"]
        EXE["Executive"]
    end

    subgraph APP["Application — 5 Product Modules"]
        M1["1. Patient & Provider<br/>Management"]
        M2["2. Telemedicine<br/>Appointments & Consultations"]
        M3["3. Remote Patient<br/>Monitoring & Alerting"]
        M4["4. AI-Assisted Health<br/>Risk Assessment"]
        M5["5. Executive Healthcare<br/>Operations Dashboard"]
    end

    subgraph PLATFORM["Platform"]
        DB[("PostgreSQL<br/>system of record")]
        CACHE[("Redis<br/>cache / de-dup")]
        AI["AI/ML Service<br/>Scikit-learn"]
    end

    subgraph CROSSCUTTING["Cross-Cutting Concerns"]
        SEC["Security<br/>JWT + OPA RBAC + Trivy"]
        OBS["Observability<br/>Prometheus + Grafana"]
    end

    USERS --> APP
    APP --> PLATFORM
    CROSSCUTTING -.-> APP
    CROSSCUTTING -.-> PLATFORM

    STD["Conceptual standards alignment:<br/>HL7 FHIR · ISO 13131/27001/27701/42001 · NIST AI RMF/CSF 2.0 · HIPAA/GDPR (conceptual) · OWASP Top 10"]
    CROSSCUTTING -.-> STD
```
