import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base

if TYPE_CHECKING:
    from app.features.user.models import User
    from app.features.registrations.models import Registration


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(120), default="Maison de Village de Martelange")

    start_at: Mapped[Optional[datetime.datetime]] = mapped_column(default=func.now())
    end_at: Mapped[Optional[datetime.datetime]] = mapped_column(default=func.now())
    capacity: Mapped[Optional[int]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="upcoming")
    banner_file_id: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=True, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(nullable=True, default=func.now())
    create_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator: Mapped["User"] = relationship(
        back_populates="created_events",
        foreign_keys=[create_by],
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
    )
