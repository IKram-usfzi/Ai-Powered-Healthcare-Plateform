from datetime import datetime, timezone

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HealthReading(Base):
    """Simulated vitals from remote monitoring. docs/backend-schema.md §2 (ADR-016: blood
    pressure stored as separate systolic/diastolic integers, not one combined field)."""

    __tablename__ = "health_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    heart_rate: Mapped[int] = mapped_column(Integer)
    systolic_bp: Mapped[int] = mapped_column(Integer)
    diastolic_bp: Mapped[int] = mapped_column(Integer)
    spo2: Mapped[int] = mapped_column(Integer)
    temperature: Mapped[float] = mapped_column(Float)
    glucose: Mapped[float] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True
    )

    patient: Mapped["Patient"] = relationship(back_populates="health_readings")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="reading")
