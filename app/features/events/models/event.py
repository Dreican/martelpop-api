from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.events.models.event_status import EventStatus
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.users.models.user import User
    from app.features.registrations.models.registration import Registration
    from app.features.storage.models.stored_file import StoredFile
    from app.features.waitlist.models.waitlist import Waitlist


class Event(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(255), default="Maison de Village de Martelange",
                                                    nullable=True)
    start_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())
    end_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())

    capacity: Mapped[Optional[int]]

    banner_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("stored_files.id"),
        nullable=True,
    )
    banner: Mapped[StoredFile | None] = relationship()

    created_by: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_events_created_by"
        )
    )

    status: Mapped[EventStatus] = relationship(
        back_populates="events"
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_events",
        foreign_keys=[created_by],
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )

    waitlist: Mapped[list["Waitlist"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )


