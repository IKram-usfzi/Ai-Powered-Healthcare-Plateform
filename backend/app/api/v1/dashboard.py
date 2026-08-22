from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.alert import Alert
from app.models.appointment import Appointment
from app.models.enums import AlertSeverity, AlertStatus, RiskCategory, UserRole
from app.models.health_reading import HealthReading
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.models.provider import Provider
from app.models.user import User
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardTrends,
    ProviderActivity,
    TopRiskPatient,
    TrendPoint,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _day_bounds(days_ago: int) -> tuple[datetime, datetime]:
    start_of_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start = start_of_today - timedelta(days=days_ago)
    return start, start + timedelta(days=1)


def _latest_predictions(db: Session) -> dict[int, Prediction]:
    latest: dict[int, Prediction] = {}
    for prediction in db.scalars(select(Prediction).order_by(Prediction.created_at)):
        latest[prediction.patient_id] = prediction  # last write wins (sorted ascending)
    return latest


def build_overview(db: Session) -> DashboardOverview:
    """Shared by GET /dashboard/overview and GET /reports/executive."""
    today_start, today_end = _day_bounds(0)
    yesterday_start, yesterday_end = _day_bounds(1)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    last_24h = datetime.now(timezone.utc) - timedelta(hours=24)

    latest_predictions = _latest_predictions(db)
    high_risk_patient_ids = {
        pid for pid, p in latest_predictions.items() if p.risk_category == RiskCategory.HIGH
    }

    top_risk = sorted(
        (p for p in latest_predictions.values() if p.risk_category == RiskCategory.HIGH),
        key=lambda p: p.confidence_score,
        reverse=True,
    )[:5]
    patients_by_id = {p.id: p for p in db.scalars(select(Patient))}
    top_risk_patients = [
        TopRiskPatient(
            patient_id=p.patient_id,
            full_name=patients_by_id[p.patient_id].full_name,
            risk_category=p.risk_category.value,
            confidence_score=p.confidence_score,
        )
        for p in top_risk
        if p.patient_id in patients_by_id
    ]

    return DashboardOverview(
        total_patients=db.scalar(select(func.count(Patient.id))) or 0,
        patients_registered_last_7_days=db.scalar(
            select(func.count(Patient.id)).where(Patient.registered_at >= seven_days_ago)
        )
        or 0,
        appointments_today=db.scalar(
            select(func.count(Appointment.id)).where(
                Appointment.scheduled_at >= today_start, Appointment.scheduled_at < today_end
            )
        )
        or 0,
        appointments_yesterday=db.scalar(
            select(func.count(Appointment.id)).where(
                Appointment.scheduled_at >= yesterday_start,
                Appointment.scheduled_at < yesterday_end,
            )
        )
        or 0,
        active_monitoring_patients=db.scalar(
            select(func.count(func.distinct(HealthReading.patient_id))).where(
                HealthReading.recorded_at >= last_24h
            )
        )
        or 0,
        high_risk_patients=len(high_risk_patient_ids),
        open_alerts=db.scalar(
            select(func.count(Alert.id)).where(Alert.status != AlertStatus.RESOLVED)
        )
        or 0,
        critical_alerts=db.scalar(
            select(func.count(Alert.id)).where(
                Alert.status != AlertStatus.RESOLVED, Alert.severity == AlertSeverity.CRITICAL
            )
        )
        or 0,
        top_risk_patients=top_risk_patients,
        appointments_today_by_status={
            status.value: count
            for status, count in db.execute(
                select(Appointment.status, func.count(Appointment.id))
                .where(
                    Appointment.scheduled_at >= today_start, Appointment.scheduled_at < today_end
                )
                .group_by(Appointment.status)
            ).all()
        },
    )


def build_trends(db: Session) -> DashboardTrends:
    """Shared by GET /dashboard/trends and GET /reports/executive."""
    points: list[TrendPoint] = []
    for days_ago in range(6, -1, -1):
        start, end = _day_bounds(days_ago)
        readings_count = (
            db.scalar(
                select(func.count(HealthReading.id)).where(
                    HealthReading.recorded_at >= start, HealthReading.recorded_at < end
                )
            )
            or 0
        )
        alerts_count = (
            db.scalar(
                select(func.count(Alert.id)).where(
                    Alert.created_at >= start, Alert.created_at < end
                )
            )
            or 0
        )
        points.append(
            TrendPoint(date=start.date(), readings_count=readings_count, alerts_count=alerts_count)
        )
    return DashboardTrends(days=points)


def build_provider_activity(db: Session) -> list[ProviderActivity]:
    """Shared by GET /dashboard/provider-activity and GET /reports/executive."""
    today_start, today_end = _day_bounds(0)
    next_7_days = datetime.now(timezone.utc) + timedelta(days=7)
    now = datetime.now(timezone.utc)

    results = []
    for provider in db.scalars(select(Provider)):
        assigned = (
            db.scalar(
                select(func.count(Patient.id)).where(Patient.assigned_provider_id == provider.id)
            )
            or 0
        )
        appts_today = (
            db.scalar(
                select(func.count(Appointment.id)).where(
                    Appointment.provider_id == provider.id,
                    Appointment.scheduled_at >= today_start,
                    Appointment.scheduled_at < today_end,
                )
            )
            or 0
        )
        upcoming = (
            db.scalar(
                select(func.count(Appointment.id)).where(
                    Appointment.provider_id == provider.id,
                    Appointment.scheduled_at >= now,
                    Appointment.scheduled_at < next_7_days,
                )
            )
            or 0
        )
        results.append(
            ProviderActivity(
                provider_id=provider.id,
                full_name=provider.full_name,
                specialty=provider.specialty,
                facility_name=provider.facility.name if provider.facility else "",
                assigned_patients=assigned,
                appointments_today=appts_today,
                upcoming_appointments_7_days=upcoming,
            )
        )
    return results


@router.get("/overview", response_model=DashboardOverview)
def dashboard_overview(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.EXECUTIVE)),
) -> DashboardOverview:
    return build_overview(db)


@router.get("/trends", response_model=DashboardTrends)
def dashboard_trends(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.EXECUTIVE)),
) -> DashboardTrends:
    return build_trends(db)


@router.get("/provider-activity", response_model=list[ProviderActivity])
def provider_activity(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMINISTRATOR, UserRole.EXECUTIVE)),
) -> list[ProviderActivity]:
    return build_provider_activity(db)
