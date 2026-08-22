from datetime import date

from pydantic import BaseModel


class TopRiskPatient(BaseModel):
    patient_id: int
    full_name: str
    risk_category: str
    confidence_score: float


class DashboardOverview(BaseModel):
    total_patients: int
    patients_registered_last_7_days: int
    appointments_today: int
    appointments_yesterday: int
    active_monitoring_patients: int
    high_risk_patients: int
    open_alerts: int
    critical_alerts: int
    top_risk_patients: list[TopRiskPatient]
    appointments_today_by_status: dict[str, int]


class TrendPoint(BaseModel):
    date: date
    readings_count: int
    alerts_count: int


class DashboardTrends(BaseModel):
    days: list[TrendPoint]


class ProviderActivity(BaseModel):
    provider_id: int
    full_name: str
    specialty: str
    facility_name: str
    assigned_patients: int
    appointments_today: int
    upcoming_appointments_7_days: int


class ExecutiveReport(BaseModel):
    generated_at: str
    overview: DashboardOverview
    trends: DashboardTrends
    provider_activity: list[ProviderActivity]
