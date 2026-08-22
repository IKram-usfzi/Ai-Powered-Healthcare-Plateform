from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Consultation(Base):
    """Record of a completed appointment. docs/backend-schema.md §2."""

    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    appointment: Mapped["Appointment"] = relationship(back_populates="consultation")
