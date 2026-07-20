from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import EVENTS_SLUG_UNIQUE
from app.core.database.mixin.slug import SlugMixin
from app.core.database.mixin.soft_delete import SoftDeleteMixin

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

    waitlist: Mapped[list["Waitlist"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )
