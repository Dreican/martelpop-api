from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.auth.enums.auth_provider import AuthProvider
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.users.models.user import User


class AuthenticationIdentity(Base, IdMixin, TimestampMixin):
    __tablename__ = "authentication_identities"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_provider_user_id"
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    password_hash: Mapped[str | None]
    provider: Mapped[AuthProvider] = mapped_column(index=True)
    provider_subject: Mapped[str]

    last_login_at: Mapped[datetime | None]

    user: Mapped["User"] = relationship(
        back_populates="authentication_identities"
    )
