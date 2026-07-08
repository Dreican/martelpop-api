from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.users.models.user import User
    from app.features.events.models.event import Event


class Waitlist(Base, IdMixin, TimestampMixin):
    __tablename__ = "waitlist"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="uq_waitlist",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False
    )
    event_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("events.id"),
        nullable=False
    )
    position: Mapped[int]
    promoted_at: Mapped[datetime | None]

    user: Mapped["User"] = relationship(
        back_populates="waitlists"
    )

    event: Mapped["Event"] = relationship(
        back_populates="waitlist"
    )
