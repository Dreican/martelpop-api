import datetime
from typing import TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .role import Role
    from .event import Event
    from .user_event import UserEvent

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(60), unique=True)
    firstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[Optional[str]]
    provider: Mapped[Optional[str]]
    provider_id: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id")
    )

    role: Mapped["Role"] = relationship(
        back_populates="user"
    )

    created_events: Mapped[list["Event"]] = relationship(
        back_populates="creator",
        foreign_keys="Event.create_by",
    )

    attendance: Mapped[list["UserEvent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"

