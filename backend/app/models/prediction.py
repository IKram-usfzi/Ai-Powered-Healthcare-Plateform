from datetime import datetime, timezone

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RiskCategory


class Prediction(Base):
    """AI risk assessment output. docs/backend-schema.md §2."""

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    risk_category: Mapped[RiskCategory] = mapped_column(Enum(RiskCategory, name="risk_category"))
    confidence_score: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(50))
    recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), index=True)

    patient: Mapped["Patient"] = relationship(back_populates="predictions")
