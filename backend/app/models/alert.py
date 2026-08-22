from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AlertSeverity, AlertStatus


class Alert(Base):
    """Abnormal-reading notification. docs/backend-schema.md §2."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    reading_id: Mapped[int] = mapped_column(ForeignKey("health_readings.id"), index=True)
    severity: Mapped[AlertSeverity] = mapped_column(Enum(AlertSeverity, name="alert_severity"))
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, name="alert_status"), default=AlertStatus.OPEN
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    patient: Mapped["Patient"] = relationship(back_populates="alerts")
    reading: Mapped["HealthReading"] = relationship(back_populates="alerts")
