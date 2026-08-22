from datetime import datetime

from pydantic import BaseModel, EmailStr


class ProviderCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    specialty: str
    facility_id: int
    license_ref: str


class ProviderRead(BaseModel):
    id: int
    full_name: str
    specialty: str
    facility_id: int
    license_ref: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AssignPatientRequest(BaseModel):
    patient_id: int
