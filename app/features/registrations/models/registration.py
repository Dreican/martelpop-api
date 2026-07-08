from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey, Text, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.events.models.event import Event
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.users.models.user import User
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin


class Registration(Base, IdMixin, TimestampMixin):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="uq_registration_user_event",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id")
    )

    event_id: Mapped[UUID] = mapped_column(
        Uuid,
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

    checked_in_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="registrations"
    )

    event: Mapped["Event"] = relationship(
        back_populates="registrations"
    )
