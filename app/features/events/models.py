from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.users.models import User
    from app.features.registrations.models import Registration
    from app.features.storage.models import StoredFile
    from app.features.waitlist.models import Waitlist


class Event(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(255), default="Maison de Village de Martelange",
                                                    nullable=True)
    start_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())
    end_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())

    capacity: Mapped[Optional[int]]

    banner_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("stored_files.id"),
        nullable=True,
    )
    banner: Mapped[StoredFile | None] = relationship()

    created_by: Mapped[int] = mapped_column(
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


class EventStatus(Base, IdMixin, TimestampMixin):
    __tablename__ = "event_statuses"

    # DRAFT = "DRAFT"
    # PUBLISHED = "PUBLISHED"
    # CANCELLED = "CANCELLED"
    # COMPLETED = "COMPLETED"

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None]
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_bookable: Mapped[bool] = mapped_column(default=True, nullable=False)
    allow_edit: Mapped[bool] = mapped_column(default=True, nullable=False)

    events: Mapped[list["Event"]] = relationship(
        back_populates="status"
    )
