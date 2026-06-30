from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from app.events.event import Event

class UserEvent(Base):
    __tablename__ = "user_events"

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

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
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