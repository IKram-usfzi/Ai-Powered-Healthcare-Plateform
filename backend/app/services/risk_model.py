import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from app.services.risk_features import FEATURE_NAMES

MODEL_DIR = Path(__file__).resolve().parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "risk_classifier.joblib"
METADATA_PATH = MODEL_DIR / "risk_classifier_metadata.json"


@lru_cache
def get_model():
    return joblib.load(MODEL_PATH)


@lru_cache
def get_metadata() -> dict:
    return json.loads(METADATA_PATH.read_text())


def predict(features: list[float]) -> tuple[str, float]:
    """Returns (risk_category, confidence_score). DataFrame column names must
    match training (app/services/risk_features.FEATURE_NAMES) — the model was
    fit on a named DataFrame, so predicting from a bare array triggers a
    sklearn feature-name mismatch warning even though the values line up."""
    model = get_model()
    row = pd.DataFrame([features], columns=FEATURE_NAMES)
    probabilities = model.predict_proba(row)[0]
    classes = model.classes_
    best_index = probabilities.argmax()
    return classes[best_index], float(probabilities[best_index])
