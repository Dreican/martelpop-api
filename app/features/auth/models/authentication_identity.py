from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.auth.enums.auth_provider import AuthProvider

if TYPE_CHECKING:
    from app.features.users.models.user import User


class AuthenticationIdentity(Base):
    __tablename__ = "authentication_identities"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_auth_identity_provider_provider_user_id"
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    password_hash: Mapped[str | None]

    provider_user_id: Mapped[str | None] = mapped_column(String(255))
    provider: Mapped[AuthProvider] = mapped_column(
        Helper.enum_column(AuthProvider),
        index=True
    )

    last_login_at: Mapped[datetime | None]

    user: Mapped["User"] = relationship(
        back_populates="authentication_identities"
    )
