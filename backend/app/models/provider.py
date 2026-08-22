from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Provider(Base):
    """Physician. docs/backend-schema.md §2."""

    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    specialty: Mapped[str] = mapped_column(String(255))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    license_ref: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="provider")
    facility: Mapped["Facility"] = relationship(back_populates="providers")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="provider")
