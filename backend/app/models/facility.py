from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Facility(Base):
    """Healthcare facility. docs/backend-schema.md §2."""

    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(255))

    providers: Mapped[list["Provider"]] = relationship(back_populates="facility")
