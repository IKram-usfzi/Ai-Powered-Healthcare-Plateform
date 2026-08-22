from datetime import datetime

from pydantic import BaseModel

from app.models.enums import AlertSeverity, AlertStatus


class HealthReadingCreate(BaseModel):
    heart_rate: int
    systolic_bp: int
    diastolic_bp: int
    spo2: int
    temperature: float
    glucose: float


class HealthReadingRead(BaseModel):
    id: int
    patient_id: int
    heart_rate: int
    systolic_bp: int
    diastolic_bp: int
    spo2: int
    temperature: float
    glucose: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class AlertRead(BaseModel):
    id: int
    patient_id: int
    reading_id: int
    severity: AlertSeverity
    status: AlertStatus
    created_at: datetime

    model_config = {"from_attributes": True}
