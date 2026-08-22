# AI Evaluation Report — Health Risk Classifier

**Related:** `docs/Testing-startegy.md` §3, `docs/api-spec.md` §6, `docs/deccission.md` ADR-005/ADR-021
**Generated:** 2026-08-22T08:39:27.801352+00:00 by `backend/scripts/train_risk_model.py`
**Model version:** `risk-rf-v1-20260822`

> **Decision-support only.** This model predicts a synthetic risk-scoring heuristic used as a
> training-label stand-in (`app/services/risk_labels.py`), not a real clinical outcome. Output is
> never a diagnosis and always requires human clinical judgement (`docs/PRD.md` §7).

## 1. Data

- 957 `health_readings` rows (one per reading, not deduplicated per patient) + age derived from each patient's `date_of_birth`
- Source: Synthea-derived seed data (`docs/backend-schema.md` §6)
- Label distribution: {'low': 889, 'moderate': 65, 'high': 3}
- Train/test split: 765/192 (80/20, stratified, `random_state=42`)

## 2. Model

- Algorithm: RandomForestClassifier (`n_estimators=100`, `max_depth=6`, `class_weight="balanced"`)
- Features (fixed order, shared with inference — `app/services/risk_features.py`): age_years, heart_rate, systolic_bp, diastolic_bp, spo2, temperature, glucose

## 3. Evaluation (held-out test set)

| Metric | Value |
|---|---|
| Accuracy | 0.995 |
| Precision (macro) | 0.643 |
| Recall (macro) | 0.667 |
| F1 (macro) | 0.654 |

### Confusion matrix (rows = actual, columns = predicted; labels: ['high', 'low', 'moderate'])

```
[[  0   0   1]
 [  0 178   0]
 [  0   0  13]]
```

### Per-class report

```
              precision    recall  f1-score   support

        high       0.00      0.00      0.00         1
         low       1.00      1.00      1.00       178
    moderate       0.93      1.00      0.96        13

    accuracy                           0.99       192
   macro avg       0.64      0.67      0.65       192
weighted avg       0.99      0.99      0.99       192

```

## 4. Feature importances

- `age_years`: 0.1345
- `heart_rate`: 0.042
- `systolic_bp`: 0.1477
- `diastolic_bp`: 0.2306
- `spo2`: 0.0223
- `temperature`: 0.1706
- `glucose`: 0.2524

## 5. Interpretation & limitations

- Ground truth is a rule-derived heuristic (no real clinical outcomes exist for synthetic
  patients), so these metrics measure how well the model approximates that heuristic from raw
  vitals — not real-world diagnostic accuracy.
- Class imbalance: the `high`
  category has only 3 examples in the full dataset
  (label distribution: {'low': 889, 'moderate': 65, 'high': 3}), reflecting how rare severely-abnormal
  readings are even in this synthetic sample — expected for a POC, but the per-class metrics for
  that category should be read as low-confidence, not as evidence the model performs poorly
  overall (see the confusion matrix above).
- Small sample size (957 readings) relative to a production model; adequate for a
  proof-of-concept decision-support demonstration only.
- Every prediction returned by `POST /ai/risk-assessment` carries a confidence score and an
  explicit recommendation to use clinical judgement (`docs/PRD.md` §7).
