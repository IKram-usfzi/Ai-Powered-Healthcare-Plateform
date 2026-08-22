from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.enums import UserRole
from app.models.facility import Facility
from app.models.patient import Patient
from app.models.provider import Provider
from app.models.user import User
from app.schemas.report import RegistrationReport

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
