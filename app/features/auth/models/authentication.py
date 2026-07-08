from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.auth.enums.auth_provider import AuthProvider
from app.features.users.models.user import User
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin


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
        nullable=False
    )

    password_hash: Mapped[str | None]
    provider: Mapped[AuthProvider]
    provider_user_id: Mapped[str | None]

    last_login_at: Mapped[Optional[datetime]]

    user: Mapped["User"] = relationship(
        back_populates="authentication_identity"
    )
