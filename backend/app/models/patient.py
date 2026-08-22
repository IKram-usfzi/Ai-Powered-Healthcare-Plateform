from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Patient(Base):
    """Patient profile, may link to a users record. docs/backend-schema.md §2."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(50))
    contact_info: Mapped[str] = mapped_column(String(255))
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # ADR-018: closes the gap between api-spec.md's POST /providers/{id}/assign-patient
    # and the original schema, which had no field to persist an assignment.
    assigned_provider_id: Mapped[int | None] = mapped_column(ForeignKey("providers.id"), index=True)

    user: Mapped["User"] = relationship(back_populates="patient")
    assigned_provider: Mapped["Provider"] = relationship(
        back_populates="assigned_patients", foreign_keys=[assigned_provider_id]
    )
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")
    health_readings: Mapped[list["HealthReading"]] = relationship(back_populates="patient")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="patient")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="patient")
