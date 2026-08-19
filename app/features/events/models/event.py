from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import EVENTS_SLUG_UNIQUE
from app.core.database.helpers import Helper
from app.core.database.mixin.slug import SlugMixin
from app.core.database.mixin.soft_delete import SoftDeleteMixin
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_status_code import EventStatusCode

if TYPE_CHECKING:
    from app.features.users.models.user import User
    from app.features.registrations.models.registration import Registration
    from app.features.storage.models.stored_file import StoredFile
    from app.features.waitlist.models.waitlist import Waitlist
    from app.features.events.models.activity_type import ActivityType
    from app.features.events.models.event_status import EventStatus


class Event(Base, SoftDeleteMixin, SlugMixin):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("slug", name=EVENTS_SLUG_UNIQUE),
    )

    activity_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("activity_types.id"),
        nullable=False,
    )

    activity_type: Mapped["ActivityType"] = relationship(
        back_populates="events",
        foreign_keys=[activity_type_id]
    )

    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)

    description: Mapped[str | None]

    location: Mapped[str | None] = mapped_column(
        String(255), default="Maison de Village de Martelange",
    )

    start_at: Mapped[datetime | None] = mapped_column(default=func.now())
    end_at: Mapped[datetime | None] = mapped_column(default=func.now())

    capacity: Mapped[int | None]

    published_at: Mapped[datetime | None]
    cancelled_at: Mapped[datetime | None]
    completed_at: Mapped[datetime | None]

    audience: Mapped[EventAudience] = mapped_column(
        Helper.enum_column(EventAudience),
        nullable=False,
        default=EventAudience.PUBLIC,
    )

    banner_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("stored_files.id"),
    )
    banner: Mapped[StoredFile | None] = relationship(
        foreign_keys=[banner_file_id],
    )

    created_by: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_events_created_by"
        )
    )
    creator: Mapped["User"] = relationship(
        back_populates="created_events",
        foreign_keys=[created_by],
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("event_statuses.id"),
    )
    status: Mapped[EventStatus] = relationship(
        back_populates="events",
        foreign_keys=[status_id],
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )

    waitlists: Mapped[list["Waitlist"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )

    @property
    def is_full(self) -> bool:
        return self.capacity is not None and (self.remaining_capacity <= 0)

    @property
    def remaining_capacity(self) -> int | None:
        if self.capacity is None:
            return None

        return self.capacity - len(self.registrations)

    @property
    def is_waitlisted(self) -> bool:
        return len(self.waitlists) > 0

    @property
    def is_cancelled(self) -> bool:
        return self.status.code == EventStatusCode.CANCELLED

    @property
    def is_draft(self) -> bool:
        return self.status.code == EventStatusCode.DRAFT

    @property
    def is_published(self) -> bool:
        return self.status.code == EventStatusCode.PUBLISHED

    @property
    def is_completed(self) -> bool:
        return self.status.code == EventStatusCode.COMPLETED

    @property
    def is_vip_event(self) -> bool:
        return self.audience == EventAudience.VIP

    @property
    def is_public(self) -> bool:
        return self.audience == EventAudience.PUBLIC

    @property
    def is_registration_open(self) -> bool:
        return self.status.is_bookable

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def update(self, title: str, description: str, location: str, start_at: datetime, end_at: datetime, capacity: int):
        self.title = title
        self.description = description
        self.location = location
        self.start_at = start_at
        self.end_at = end_at
        self.capacity = capacity

    def publish(self, event_status: EventStatus) -> None:
        self.status = event_status
        self.published_at = datetime.now(UTC)

    def cancel(self, event_status: EventStatus) -> None:
        self.status = event_status
        self.cancelled_at = datetime.now(UTC)

    def complete(self, event_status: EventStatus) -> None:
        self.status = event_status
        self.completed_at = datetime.now(UTC)

    def unpublish(self, event_status: EventStatus) -> None:
        self.status = event_status
        self.published_at = None
        self.cancelled_at = None
        self.completed_at = None

    def delete(self, event_status: EventStatus) -> None:
        self.cancel(event_status)
        self.deleted_at = datetime.now(UTC)

    def is_owner(self, principal: AuthenticatedPrincipal) -> bool:
        return self.created_by == principal.user.id
