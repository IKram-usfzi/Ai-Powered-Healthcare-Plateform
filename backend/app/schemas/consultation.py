from datetime import datetime

from pydantic import BaseModel


class ConsultationCreate(BaseModel):
    appointment_id: int
    summary: str
    recommendations: str


class ConsultationRead(BaseModel):
    id: int
    appointment_id: int
    summary: str
    recommendations: str
    created_at: datetime

    model_config = {"from_attributes": True}
