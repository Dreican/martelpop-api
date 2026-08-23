from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import SYSTEM_USER_ID
from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import (
    RegistrationAlreadyCancelledError,
    RegistrationPromoteError, RegistrationUncancelledError
)

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

    registered_at: Mapped[datetime | None]
    registered_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_registrations_registered_by",
        ),
    )

    registered_by: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[registered_by_id],
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

    waitlisted_at: Mapped[datetime | None]
    waitlisted_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_registrations_waitlisted_by",
        ),
    )
    waitlisted_by: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[waitlisted_by_id],
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

    def promote(self):
        if self.status is not RegistrationStatus.WAITLISTED:
            raise RegistrationPromoteError("Only a waitlisted registration can be promoted")

        self.registered_at = datetime.now(UTC)
        self.registered_by_id = SYSTEM_USER_ID
        self.status = RegistrationStatus.REGISTERED

    def cancel(self, user: User):
        if self.status is RegistrationStatus.CANCELLED:
            raise RegistrationAlreadyCancelledError()

        self.cancelled_at = datetime.now(UTC)
        self.cancelled_by = user
        self.status = RegistrationStatus.CANCELLED

    def uncancel(self, user: User):
        if self.status is not RegistrationStatus.CANCELLED:
            raise RegistrationUncancelledError("Only a cancelled registration can be uncancelled.")

        self.cancelled_at = None
        self.cancelled_by = None
        self.status = RegistrationStatus.REGISTERED
        self.registered_at = datetime.now(UTC)
        self.registered_by = user

    def waitlist(self, user: User):
        self.cancelled_at = None
        self.cancelled_by = None
        self.status = RegistrationStatus.WAITLISTED
        self.waitlisted_at = datetime.now(UTC)
        self.waitlisted_by = user

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled_at is not None

    def is_owner(self, principal: AuthenticatedPrincipal) -> bool:
        return self.user_id == principal.user.id



    @staticmethod
    def create(event: Event, user: User, note: str | None, status: RegistrationStatus, registered_by_id: UUID):
        registration = Registration(
            event=event,
            user=user,
            note=note,
            status=status,
            registered_by_id=registered_by_id,
            registered_at=datetime.now(UTC)
        )
        return registration
