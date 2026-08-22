from datetime import date, datetime

from pydantic import BaseModel


class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    contact_info: str


class PatientUpdate(BaseModel):
    full_name: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    contact_info: str | None = None


class PatientRead(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    gender: str
    contact_info: str
    registered_at: datetime
    assigned_provider_id: int | None

    model_config = {"from_attributes": True}
