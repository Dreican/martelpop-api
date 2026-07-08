from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import String, ForeignKey, Enum, Uuid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.auth.models.role import Role
    from app.features.events.models.event import Event
    from app.features.registrations.models.registration import Registration
    from app.features.storage.models.stored_file import StoredFile
    from app.features.users.enums.user_status import UserStatus
    from app.features.auth.models.authentication import AuthenticationIdentity
    from app.features.waitlist.models.waitlist import Waitlist


class User(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)

    avatar_file_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "stored_files.id",
            name="fk_users_avatar_file"
        ),
        nullable=True
    )

    avatar: Mapped[StoredFile | None] = relationship()
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        default=UserStatus.ACTIVE
    )

    role_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("roles.id")
    )

    role: Mapped["Role"] = relationship(
        back_populates="users"
    )

    created_events: Mapped[list["Event"]] = relationship(
        back_populates="creator",
        foreign_keys="Event.created_by"
    )

    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    waitlists: Mapped[list["Waitlist"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    auth_identities: Mapped[list["AuthenticationIdentity"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"
