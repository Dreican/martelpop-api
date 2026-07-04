from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func, BigInteger, Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.events.enums import EventStatus
from app.features.storage.models import StoredFile
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.user.models import User
    from app.features.registrations.models import Registration


class Event(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(255), default="Maison de Village de Martelange")

    start_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())
    end_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())

    capacity: Mapped[Optional[int]]
    status: Mapped[EventStatus] = mapped_column(
        Enum(
            EventStatus,
            name="event_status"
        ),
        default=EventStatus.DRAFT
    )
    banner_file_id: Mapped[int | None] = mapped_column(
        foreign_keys="stored_files.id",
        nullable=True,
        name="fk_events_banner_file"
    )
    banner: Mapped[StoredFile | None] = relationship()

    create_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        name="fk_events_created_by"
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_events",
        foreign_keys=[create_by],
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )
