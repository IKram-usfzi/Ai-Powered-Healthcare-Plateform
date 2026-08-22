import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.core.redis_client import get_redis
from app.models.alert import Alert
from app.models.enums import AlertStatus, UserRole
from app.models.health_reading import HealthReading
from app.models.patient import Patient
from app.models.user import User
from app.schemas.monitoring import AlertRead, HealthReadingCreate, HealthReadingRead
from app.services.vitals import evaluate_severity

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

# docs/flow.md §3: an abnormal reading triggers at most one open alert per
# patient within this window, de-duplicated via Redis (ADR-002).
ALERT_DEDUP_TTL_SECONDS = 300


def _dedup_key(patient_id: int) -> str:
    return f"alert:dedup:{patient_id}"


@router.post("/readings", response_model=HealthReadingRead, status_code=status.HTTP_201_CREATED)
def ingest_reading(
    payload: HealthReadingCreate,
    db: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.PATIENT)),
) -> HealthReading:
    if current_user.patient is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No patient record linked to this user"
        )

    reading = HealthReading(patient_id=current_user.patient.id, **payload.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)

    severity = evaluate_severity(
        heart_rate=reading.heart_rate,
        systolic_bp=reading.systolic_bp,
        diastolic_bp=reading.diastolic_bp,
        spo2=reading.spo2,
        temperature=reading.temperature,
        glucose=reading.glucose,
    )
    if severity is not None and redis_client.get(_dedup_key(reading.patient_id)) is None:
        db.add(Alert(patient_id=reading.patient_id, reading_id=reading.id, severity=severity))
        db.commit()
        redis_client.set(_dedup_key(reading.patient_id), "1", ex=ALERT_DEDUP_TTL_SECONDS)

    return reading


@router.get("/readings/{patient_id}", response_model=list[HealthReadingRead])
def get_reading_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR, UserRole.PATIENT)
    ),
) -> list[HealthReading]:
    if current_user.role == UserRole.PATIENT:
        if current_user.patient is None or current_user.patient.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this patient's readings",
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
                detail="You do not have permission to view this patient's readings",
            )

    stmt = select(HealthReading).where(HealthReading.patient_id == patient_id)
    return list(db.scalars(stmt))


@router.get("/alerts", response_model=list[AlertRead])
def list_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.DOCTOR, UserRole.ADMINISTRATOR)),
) -> list[Alert]:
    stmt = select(Alert).where(Alert.status != AlertStatus.RESOLVED)
    if current_user.role == UserRole.DOCTOR:
        if current_user.provider is None:
            return []
        stmt = stmt.join(Patient, Alert.patient_id == Patient.id).where(
            Patient.assigned_provider_id == current_user.provider.id
        )
    return list(db.scalars(stmt))


@router.patch("/alerts/{alert_id}/acknowledge", response_model=AlertRead)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.DOCTOR)),
) -> Alert:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    patient = db.get(Patient, alert.patient_id)
    if (
        patient is None
        or current_user.provider is None
        or patient.assigned_provider_id != current_user.provider.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to acknowledge this alert",
        )

    alert.status = AlertStatus.ACKNOWLEDGED
    db.commit()
    db.refresh(alert)
    return alert
