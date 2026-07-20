from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.features.registrations.enums.registration_status import RegistrationStatus

if TYPE_CHECKING:
    from app.features.users.models.user import User
    from app.features.events.models.event import Event


class Registration(Base):
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

    checked_in_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="checked_in_registrations",
        foreign_keys=[checked_in_by]
    )

    user: Mapped["User"] = relationship(
        back_populates="registrations",
        foreign_keys=[user_id]
    )

    event: Mapped["Event"] = relationship(
        back_populates="registrations"
    )
