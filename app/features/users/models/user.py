from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import USERS_EMAIL_UNIQUE, USERS_SLUG_UNIQUE
from app.core.database.mixin.id import IdMixin
from app.core.database.mixin.slug import SlugMixin
from app.core.database.mixin.soft_delete import SoftDeleteMixin
from app.core.database.mixin.timestamp import TimestampMixin
from app.features.users.enums.user_status import UserStatus

if TYPE_CHECKING:
    from app.features.auth.models.refresh_token import RefreshToken
    from app.features.auth.models.role import Role
    from app.features.events.models.event import Event
    from app.features.registrations.models.registration import Registration
    from app.features.storage.models.stored_file import StoredFile
    from app.features.auth.models.authentication_identity import AuthenticationIdentity
    from app.features.waitlist.models.waitlist import Waitlist


class User(Base, IdMixin, TimestampMixin, SoftDeleteMixin, SlugMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name=USERS_EMAIL_UNIQUE),
        UniqueConstraint("slug", name=USERS_SLUG_UNIQUE),
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))

    avatar_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "stored_files.id",
            name="fk_users_avatar_file",
            use_alter=True,
        ),
    )
    avatar: Mapped["StoredFile | None"] = relationship(
        "StoredFile",
        foreign_keys=[avatar_file_id],
        post_update=True,
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE.value
    )

    role_id: Mapped[UUID] = mapped_column(
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
        foreign_keys="Registration.user_id",
        cascade="all, delete-orphan"
    )

    checked_in_registrations: Mapped[list["Registration"]] = relationship(
        "Registration",
        back_populates="checked_in_user",
        foreign_keys="Registration.checked_in_by"
    )

    waitlists: Mapped[list["Waitlist"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    authentication_identities: Mapped[list["AuthenticationIdentity"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    uploaded_files: Mapped[list["StoredFile"]] = relationship(
        "StoredFile",
        foreign_keys="StoredFile.uploaded_by_id",
        back_populates="uploaded_by",
    )

    @hybrid_property
    def fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"
