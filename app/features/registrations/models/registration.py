from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey, Text, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.registrations.enums.registration_status import RegistrationStatus
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.users.models.user import User
    from app.features.events.models.event import Event


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
        ForeignKey("users.id")
    )

    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("events.id")
    )

    note: Mapped[str | None]

    status: Mapped[RegistrationStatus] = mapped_column(default=RegistrationStatus.REGISTERED)

    cancelled_at: Mapped[datetime | None]

    checked_in: Mapped[bool] = mapped_column(
        default=False
    )

    checked_in_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="registrations"
    )

    event: Mapped["Event"] = relationship(
        back_populates="registrations"
    )
