from datetime import datetime

from pydantic import BaseModel

from app.models.enums import RiskCategory


class RiskAssessmentRequest(BaseModel):
    patient_id: int


class PredictionRead(BaseModel):
    id: int
    patient_id: int
    risk_category: RiskCategory
    confidence_score: float
    model_version: str
    recommendation: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ModelMetadata(BaseModel):
    model_version: str
    algorithm: str
    trained_at: str
    feature_names: list[str]
    n_samples: int
    n_train: int
    n_test: int
    label_distribution: dict[str, int]
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    feature_importances: dict[str, float]
