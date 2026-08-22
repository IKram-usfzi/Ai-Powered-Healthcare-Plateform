from pydantic import BaseModel


class RegistrationReport(BaseModel):
    total_patients: int
    total_providers: int
    total_facilities: int
    patients_registered_last_30_days: int
    unassigned_patients: int
    providers_by_specialty: dict[str, int]


class AppointmentReport(BaseModel):
    total_appointments: int
    appointments_by_status: dict[str, int]
    appointments_next_7_days: int
    total_consultations: int
