from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.users.enums import UserStatus, AuthProvider
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.features.auth.models import Role
    from app.features.events.models import Event
    from app.features.registrations.models import Registration
    from app.features.storage.models import StoredFile
    from app.features.waitlist.models import Waitlist


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

    avatar_file_id: Mapped[int | None] = mapped_column(
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

    role_id: Mapped[int] = mapped_column(
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


class AuthenticationIdentity(Base, IdMixin, TimestampMixin):
    __tablename__ = "authentication_identities"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_provider_user_id"
        ),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    password_hash: Mapped[str | None]
    provider: Mapped[AuthProvider]
    provider_user_id: Mapped[str | None]

    last_login_at: Mapped[Optional[datetime]]

    user: Mapped["User"] = relationship(
        back_populates="authentication_identity"
    )
