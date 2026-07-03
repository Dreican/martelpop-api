from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.shared.database.base import Base

if TYPE_CHECKING:
    from app.features.user.models import User
    from app.features.events.model import Event

class Registration(Base):
    __tablename__ = "registrations"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        primary_key=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="going",
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    checked_in: Mapped[bool] = mapped_column(
        default=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="attendance"
    )

    event: Mapped["Event"] = relationship(
        back_populates="attendees"
    )