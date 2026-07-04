from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey, BigInteger, Enum
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.features.user.enums import UserStatus
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.auth.models import Role
    from app.features.events.model import Event
    from app.features.registrations.models import Registration
    from app.features.storage.models import StoredFile

class User(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        Index=True
    )

    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))

    provider: Mapped[Optional[str]]
    provider_id: Mapped[Optional[str]]

    last_login_at: Mapped[Optional[datetime]]

    avatar_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("stored_files.id"),
        nullable=True,
        name="fk_users_avatar_file"
    )

    avatar: Mapped[StoredFile | None] = relationship()
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        default=UserStatus.ACTIVE
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        name="fk_users_role"
    )

    role: Mapped["Role"] = relationship(
        back_populates="user"
    )

    created_events: Mapped[list["Event"]] = relationship(
        back_populates="creator",
        foreign_keys="Event.create_by",
        name="fk_events_created_by"
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        name="fk_registrations_user"
    )

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"

