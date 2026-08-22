from datetime import date, datetime

from pydantic import BaseModel, EmailStr, model_validator


class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    contact_info: str
    # Optional: mirrors ProviderCreate (ADR-020) — creates a linked login so the
    # patient can use "self" access (GET /patients/{id}, /appointments,
    # /consultations/{patientId}, /monitoring/readings) per api-spec.md's role
    # tables. Omit both for an admin-only record with no portal access.
    email: EmailStr | None = None
    password: str | None = None

    @model_validator(mode="after")
    def _email_and_password_together(self) -> "PatientCreate":
        if bool(self.email) != bool(self.password):
            raise ValueError("email and password must be provided together, or not at all")
        return self


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
