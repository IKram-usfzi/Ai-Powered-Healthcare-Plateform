# 6. AI Health Risk Assessment Architecture Diagram

**Source:** `docs/flow.md` §4 (AI Risk Prediction Flow), `app/services/risk_features.py`, `scripts/train_risk_model.py`.

```mermaid
flowchart TB
    DOC["Doctor<br/>(assigned patients only)"] -->|"POST /ai/risk-assessment"| API

    subgraph API["FastAPI — AI Risk API"]
        FETCH["Fetch patient's recent readings"]
        FEAT["Feature extraction<br/>(app/services/risk_features.py —<br/>shared verbatim with training)"]
        INFER["Model inference"]
        STORE["Store prediction"]
    end

    PG[("PostgreSQL<br/>health_readings")] --> FETCH
    FETCH --> FEAT
    FEAT --> INFER
    MODEL["RandomForestClassifier<br/>backend/app/ml_models/*.joblib<br/>trained offline via scripts/train_risk_model.py"] --> INFER
    INFER --> STORE
    STORE --> PRED[("PostgreSQL<br/>predictions")]
    INFER -->|"category + confidence +<br/>'requires clinical judgement'<br/>recommendation"| DOC

    subgraph TRAIN["Offline training (scripts/train_risk_model.py)"]
        direction TB
        LABEL["Weighted point-score<br/>label heuristic<br/>(risk_labels.py — deliberately<br/>separate from Module 3's<br/>alert-threshold logic)"]
        RF["RandomForestClassifier<br/>n_estimators=100, max_depth=6"]
        EVAL["docs/ai-evaluation-report.md<br/>(accuracy/precision/recall/F1)"]
    end

    PG -.->|"957 health_readings rows"| LABEL
    LABEL --> RF
    RF --> EVAL
    RF -.->|"committed model artifact"| MODEL
```

`GET /ai/model/metadata` (Administrator-only) exposes the training metrics shown above. Every prediction response is explicitly framed as decision-support (`docs/PRD.md` §7) — never a diagnosis.
