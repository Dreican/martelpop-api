from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import ACTIVITY_TYPES_NAME_UNIQUE, ACTIVITY_TYPES_SLUG_UNIQUE
from app.core.database.mixin.slug import SlugMixin
from app.core.database.mixin.soft_delete import SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.events.models.event import Event
    from app.features.storage.models.stored_file import StoredFile


class ActivityType(Base, SoftDeleteMixin, SlugMixin):
    __tablename__ = "activity_types"
    __table_args__ = (
        UniqueConstraint("name", name=ACTIVITY_TYPES_NAME_UNIQUE),
        UniqueConstraint("slug", name=ACTIVITY_TYPES_SLUG_UNIQUE),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    description: Mapped[str | None] = mapped_column(Text)

    banner_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("stored_files.id")
    )
    banner: Mapped[StoredFile | None] = relationship(
        foreign_keys=[banner_file_id],
    )

    icon_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("stored_files.id"),
    )
    icon: Mapped[StoredFile | None] = relationship(
        foreign_keys=[icon_file_id],
    )

    color: Mapped[str | None] = mapped_column(String(7))

    default_location: Mapped[str | None] = mapped_column(String(255))
    default_capacity: Mapped[int | None]
    default_duration_minutes: Mapped[int | None]

    events: Mapped[list["Event"]] = relationship(
        back_populates="activity_type",
    )
