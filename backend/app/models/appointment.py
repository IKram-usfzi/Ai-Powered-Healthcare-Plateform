from datetime import datetime, timezone

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AppointmentStatus


class Appointment(Base):
    """Scheduled telemedicine session. docs/backend-schema.md §2."""

    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), index=True)
    scheduled_at: Mapped[datetime] = mapped_column(index=True)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus, name="appointment_status"),
        default=AppointmentStatus.SCHEDULED,
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    provider: Mapped["Provider"] = relationship(back_populates="appointments")
    consultation: Mapped["Consultation"] = relationship(back_populates="appointment", uselist=False)
