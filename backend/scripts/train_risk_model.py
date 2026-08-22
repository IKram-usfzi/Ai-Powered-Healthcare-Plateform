"""Train the Module 4 health-risk classifier (docs/api-spec.md §6, ADR-005/ADR-021).

Pulls each patient's most recent health_reading from the database, derives
age from date_of_birth, and builds a supervised training set by labeling each
row with app/services/risk_labels.py's point-score heuristic (a stand-in for
real clinical outcomes, since none exist for synthetic patients — output is
decision-support only, never a diagnosis, per docs/PRD.md §7).

Trains a RandomForestClassifier, evaluates it with a held-out test split
(accuracy/precision/recall/F1 per class + confusion matrix, per
docs/Testing-startegy.md §3), and writes:
  - backend/app/ml_models/risk_classifier.joblib   (the trained model)
  - backend/app/ml_models/risk_classifier_metadata.json (for GET /ai/model/metadata)
  - docs/ai-evaluation-report.md                    (the AI evaluation report deliverable)

Usage:
    python scripts/train_risk_model.py
"""

import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.db.base import SessionLocal  # noqa: E402
from app.models.health_reading import HealthReading  # noqa: E402
from app.models.patient import Patient  # noqa: E402
from app.services.risk_features import FEATURE_NAMES, age_years, extract_features  # noqa: E402
from app.services.risk_labels import bucket_score, risk_score  # noqa: E402

MODEL_DIR = Path(__file__).resolve().parent.parent / "app" / "ml_models"
MODEL_PATH = MODEL_DIR / "risk_classifier.joblib"
METADATA_PATH = MODEL_DIR / "risk_classifier_metadata.json"
DOCS_DIR = Path(
    os.environ.get("DOCS_DIR") or Path(__file__).resolve().parent.parent.parent / "docs"
)
REPORT_PATH = DOCS_DIR / "ai-evaluation-report.md"

MODEL_VERSION = f"risk-rf-v1-{datetime.now(timezone.utc):%Y%m%d}"


def build_dataset(session) -> pd.DataFrame:
    """One row per health_reading (not deduplicated to one per patient) — this
    both gives a larger training set and, since spo2/temperature are only
    real for ~5% of Synthea encounters (docs/backend-schema.md §6) and mostly
    simulated as normal otherwise, meaningfully more moderate/high examples
    for the rarer categories than a one-row-per-patient (latest reading only)
    dataset would."""
    patients = {p.id: p for p in session.scalars(select(Patient))}

    rows = []
    for reading in session.scalars(select(HealthReading)):
        patient = patients.get(reading.patient_id)
        if patient is None:
            continue
        age = age_years(patient.date_of_birth, date.today())
        features = extract_features(
            age=age,
            heart_rate=reading.heart_rate,
            systolic_bp=reading.systolic_bp,
            diastolic_bp=reading.diastolic_bp,
            spo2=reading.spo2,
            temperature=reading.temperature,
            glucose=reading.glucose,
        )
        label = bucket_score(
            risk_score(
                age=age,
                heart_rate=reading.heart_rate,
                systolic_bp=reading.systolic_bp,
                diastolic_bp=reading.diastolic_bp,
                spo2=reading.spo2,
                temperature=reading.temperature,
                glucose=reading.glucose,
            )
        ).value
        rows.append({**dict(zip(FEATURE_NAMES, features, strict=True)), "risk_category": label})

    return pd.DataFrame(rows)


def train() -> None:
    session = SessionLocal()
    df = build_dataset(session)
    session.close()

    if len(df) < 20:
        raise SystemExit(
            f"Only {len(df)} readings found — need seed data first (scripts/seed_synthea.py)."
        )

    print(f"Dataset: {len(df)} readings, label distribution {Counter(df['risk_category'])}")

    X = df[FEATURE_NAMES]
    y = df["risk_category"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100, max_depth=6, class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    report_text = classification_report(y_test, y_pred, labels=labels, zero_division=0)

    print(
        f"Accuracy: {accuracy:.3f}  Precision(macro): {precision:.3f}  "
        f"Recall(macro): {recall:.3f}  F1(macro): {f1:.3f}"
    )
    print(report_text)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metadata = {
        "model_version": MODEL_VERSION,
        "algorithm": "RandomForestClassifier",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "feature_names": FEATURE_NAMES,
        "n_samples": len(df),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "label_distribution": dict(Counter(df["risk_category"])),
        "accuracy": round(accuracy, 4),
        "precision_macro": round(precision, 4),
        "recall_macro": round(recall, 4),
        "f1_macro": round(f1, 4),
        "feature_importances": dict(
            zip(FEATURE_NAMES, [round(v, 4) for v in model.feature_importances_], strict=True)
        ),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2))

    report_md = f"""# AI Evaluation Report — Health Risk Classifier

**Related:** `docs/Testing-startegy.md` §3, `docs/api-spec.md` §6, `docs/deccission.md` ADR-005/ADR-021
**Generated:** {metadata['trained_at']} by `backend/scripts/train_risk_model.py`
**Model version:** `{MODEL_VERSION}`

> **Decision-support only.** This model predicts a synthetic risk-scoring heuristic used as a
> training-label stand-in (`app/services/risk_labels.py`), not a real clinical outcome. Output is
> never a diagnosis and always requires human clinical judgement (`docs/PRD.md` §7).

## 1. Data

- {len(df)} `health_readings` rows (one per reading, not deduplicated per patient) + age derived from each patient's `date_of_birth`
- Source: Synthea-derived seed data (`docs/backend-schema.md` §6)
- Label distribution: {metadata['label_distribution']}
- Train/test split: {len(X_train)}/{len(X_test)} (80/20, stratified, `random_state=42`)

## 2. Model

- Algorithm: RandomForestClassifier (`n_estimators=100`, `max_depth=6`, `class_weight="balanced"`)
- Features (fixed order, shared with inference — `app/services/risk_features.py`): {", ".join(FEATURE_NAMES)}

## 3. Evaluation (held-out test set)

| Metric | Value |
|---|---|
| Accuracy | {accuracy:.3f} |
| Precision (macro) | {precision:.3f} |
| Recall (macro) | {recall:.3f} |
| F1 (macro) | {f1:.3f} |

### Confusion matrix (rows = actual, columns = predicted; labels: {labels})

```
{cm}
```

### Per-class report

```
{report_text}
```

## 4. Feature importances

{chr(10).join(f"- `{name}`: {value}" for name, value in metadata["feature_importances"].items())}

## 5. Interpretation & limitations

- Ground truth is a rule-derived heuristic (no real clinical outcomes exist for synthetic
  patients), so these metrics measure how well the model approximates that heuristic from raw
  vitals — not real-world diagnostic accuracy.
- Class imbalance: the `{min(metadata['label_distribution'], key=metadata['label_distribution'].get)}`
  category has only {min(metadata['label_distribution'].values())} examples in the full dataset
  (label distribution: {metadata['label_distribution']}), reflecting how rare severely-abnormal
  readings are even in this synthetic sample — expected for a POC, but the per-class metrics for
  that category should be read as low-confidence, not as evidence the model performs poorly
  overall (see the confusion matrix above).
- Small sample size ({len(df)} readings) relative to a production model; adequate for a
  proof-of-concept decision-support demonstration only.
- Every prediction returned by `POST /ai/risk-assessment` carries a confidence score and an
  explicit recommendation to use clinical judgement (`docs/PRD.md` §7).
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report_md)

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metadata to {METADATA_PATH}")
    print(f"Saved AI evaluation report to {REPORT_PATH}")


if __name__ == "__main__":
    train()
