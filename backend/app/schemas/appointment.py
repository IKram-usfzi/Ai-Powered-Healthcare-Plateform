from datetime import datetime

from pydantic import BaseModel

from app.models.enums import AppointmentStatus


class AppointmentCreate(BaseModel):
    provider_id: int
    scheduled_at: datetime
    patient_id: int | None = None  # Administrator only; Patient always books for self


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    provider_id: int
    scheduled_at: datetime
    status: AppointmentStatus
    created_at: datetime

    model_config = {"from_attributes": True}
