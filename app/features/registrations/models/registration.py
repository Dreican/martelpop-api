from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.auth.security.principal import AuthenticatedPrincipal
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

    status: Mapped[RegistrationStatus] = mapped_column(
        Helper.enum_column(RegistrationStatus),
        nullable=False,
    )

    cancelled_at: Mapped[datetime | None]
    cancelled_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_registrations_cancelled_by",
        ),
    )

    cancelled_by: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[cancelled_by_id],
    )

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

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled_at is not None

    def is_owner(self, principal: AuthenticatedPrincipal) -> bool:
        return self.user_id == principal.user.id

    def cancel(self, user: User):
        self.cancelled_at = datetime.now()
        self.cancelled_by = user
        self.status = RegistrationStatus.CANCELLED

    def uncancel(self):
        self.cancelled_at = None
        self.cancelled_by = None
        self.status = RegistrationStatus.REGISTERED

    @staticmethod
    def create(event: Event, user: User, note: str | None, status: RegistrationStatus):
        registration = Registration(
            event=event,
            user=user,
            note=note,
            status=status
        )
        return registration
