from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.events.models.event import Event


class EventStatus(Base, IdMixin, TimestampMixin):
    __tablename__ = "event_statuses"

    # DRAFT = "DRAFT"
    # PUBLISHED = "PUBLISHED"
    # CANCELLED = "CANCELLED"
    # COMPLETED = "COMPLETED"

    code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None]
    sort_order: Mapped[int] = mapped_column(default=0)
    is_public: Mapped[bool] = mapped_column(default=True)
    is_bookable: Mapped[bool] = mapped_column(default=True)
    allow_edit: Mapped[bool] = mapped_column(default=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="status"
    )
