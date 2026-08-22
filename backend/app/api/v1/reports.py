from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.api.v1.dashboard import build_overview, build_provider_activity, build_trends
from app.models.appointment import Appointment
from app.models.consultation import Consultation
from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.patient import Patient
from app.models.provider import Provider
from app.models.user import User
from app.schemas.dashboard import ExecutiveReport
from app.schemas.report import AppointmentReport, RegistrationReport

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/registration", response_model=RegistrationReport)
def registration_report(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.EXECUTIVE)),
) -> RegistrationReport:
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    specialty_rows = db.execute(
        select(Provider.specialty, func.count(Provider.id)).group_by(Provider.specialty)
    ).all()

    return RegistrationReport(
        total_patients=db.scalar(select(func.count(Patient.id))) or 0,
        total_providers=db.scalar(select(func.count(Provider.id))) or 0,
        total_facilities=db.scalar(select(func.count(Facility.id))) or 0,
        patients_registered_last_30_days=db.scalar(
            select(func.count(Patient.id)).where(Patient.registered_at >= thirty_days_ago)
        )
        or 0,
        unassigned_patients=db.scalar(
            select(func.count(Patient.id)).where(Patient.assigned_provider_id.is_(None))
        )
        or 0,
        providers_by_specialty={specialty: count for specialty, count in specialty_rows},
    )


@router.get("/appointments", response_model=AppointmentReport)
def appointment_report(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.EXECUTIVE)),
) -> AppointmentReport:
    now = datetime.now(timezone.utc)
    next_7_days = now + timedelta(days=7)

    status_rows = db.execute(
        select(Appointment.status, func.count(Appointment.id)).group_by(Appointment.status)
    ).all()

    return AppointmentReport(
        total_appointments=db.scalar(select(func.count(Appointment.id))) or 0,
        appointments_by_status={status.value: count for status, count in status_rows},
        appointments_next_7_days=db.scalar(
            select(func.count(Appointment.id)).where(
                Appointment.scheduled_at >= now, Appointment.scheduled_at < next_7_days
            )
        )
        or 0,
        total_consultations=db.scalar(select(func.count(Consultation.id))) or 0,
    )


@router.get("/executive", response_model=ExecutiveReport)
def executive_report(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.EXECUTIVE)),
) -> ExecutiveReport:
    """UIUX.md §3.2 'Export Data' button on the Unified Dashboard."""
    return ExecutiveReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        overview=build_overview(db),
        trends=build_trends(db),
        provider_activity=build_provider_activity(db),
    )
