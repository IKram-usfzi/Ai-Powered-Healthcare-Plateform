from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.enums import RiskCategory, UserRole
from app.models.health_reading import HealthReading
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.ai import ModelMetadata, PredictionRead, RiskAssessmentRequest
from app.services.risk_features import age_years, extract_features
from app.services.risk_model import get_metadata, predict

router = APIRouter(prefix="/ai", tags=["ai"])

RECOMMENDATIONS = {
    RiskCategory.LOW: (
        "Vitals within expected range. Continue routine monitoring. "
        "AI-assisted output — always requires clinical judgement."
    ),
    RiskCategory.MODERATE: (
        "Some vitals outside normal range. Recommend clinical review within a few days. "
        "AI-assisted output — always requires clinical judgement."
    ),
    RiskCategory.HIGH: (
        "Multiple vitals significantly abnormal. Recommend urgent clinical review. "
        "AI-assisted output — always requires clinical judgement."
    ),
}


def _model_unavailable() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Risk model not available — run scripts/train_risk_model.py first",
    )


@router.post("/risk-assessment", response_model=PredictionRead, status_code=status.HTTP_201_CREATED)
def run_risk_assessment(
    payload: RiskAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.DOCTOR)),
) -> Prediction:
    patient = db.get(Patient, payload.patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if current_user.provider is None or patient.assigned_provider_id != current_user.provider.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to assess this patient",
        )

    reading = db.scalar(
        select(HealthReading)
        .where(HealthReading.patient_id == patient.id)
        .order_by(HealthReading.recorded_at.desc())
        .limit(1)
    )
    if reading is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No vitals recorded for this patient yet",
        )

    try:
        metadata = get_metadata()
        features = extract_features(
            age=age_years(patient.date_of_birth, date.today()),
            heart_rate=reading.heart_rate,
            systolic_bp=reading.systolic_bp,
            diastolic_bp=reading.diastolic_bp,
            spo2=reading.spo2,
            temperature=reading.temperature,
            glucose=reading.glucose,
        )
        risk_category, confidence = predict(features)
    except FileNotFoundError as exc:
        raise _model_unavailable() from exc

    category = RiskCategory(risk_category)
    prediction = Prediction(
        patient_id=patient.id,
        risk_category=category,
        confidence_score=confidence,
        model_version=metadata["model_version"],
        recommendation=RECOMMENDATIONS[category],
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/predictions/{patient_id}", response_model=list[PredictionRead])
def get_prediction_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR, UserRole.PATIENT)
    ),
) -> list[Prediction]:
    if current_user.role == UserRole.PATIENT:
        if current_user.patient is None or current_user.patient.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view these predictions",
            )
    elif current_user.role == UserRole.DOCTOR:
        patient = db.get(Patient, patient_id)
        if (
            patient is None
            or current_user.provider is None
            or patient.assigned_provider_id != current_user.provider.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view these predictions",
            )

    stmt = select(Prediction).where(Prediction.patient_id == patient_id)
    return list(db.scalars(stmt))


@router.get("/model/metadata", response_model=ModelMetadata)
def model_metadata(
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> dict:
    try:
        return get_metadata()
    except FileNotFoundError as exc:
        raise _model_unavailable() from exc
