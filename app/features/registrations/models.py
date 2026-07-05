from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.features.registrations.enums import RegistrationStatus
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.users.models import User
    from app.features.events.models import Event


class Registration(Base, IdMixin, TimestampMixin):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="uq_registration_user_event",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id")
    )

    note: Mapped[Optional[str]] = mapped_column(Text)

    status: Mapped[RegistrationStatus]

    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    checked_in: Mapped[bool] = mapped_column(
        default=False
    )

    checked_in_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="registrations"
    )

    event: Mapped["Event"] = relationship(
        back_populates="registrations"
    )
