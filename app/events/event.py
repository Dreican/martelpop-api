import datetime
from typing import TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey, Text, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.user_event import UserEvent

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(120), default="Maison de Village de Martelange")
    start_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(default=func.now())
    end_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(default=func.now())
    max_participants: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    create_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator: Mapped["User"] = relationship(
        back_populates="created_events",
        foreign_keys=[create_by],
    )

    attendees: Mapped[list["UserEvent"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )
