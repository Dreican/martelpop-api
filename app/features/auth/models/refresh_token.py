from datetime import datetime, UTC
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.database.base import Base
from app.core.database.mixin.id import IdMixin
from app.core.database.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.features.users.models.user import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    __table_args__ = (
        Index("ix_refresh_tokens_user_active",
              "user_id",
              "revoked_at",
              ),

    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    jti: Mapped[UUID] = mapped_column(
        default=uuid4,
        index=True,
        unique=True,
    )

    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    device_name: Mapped[str | None]

    expires_at: Mapped[datetime] = mapped_column(index=True)
    revoked_at: Mapped[datetime | None]
    last_used_at: Mapped[datetime | None]
    replaced_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("refresh_tokens.id", ondelete="SET NULL")
    )

    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens",
    )

    replaced_by: Mapped["RefreshToken | None"] = relationship(
        remote_side=lambda: [RefreshToken.id],
        uselist=False
    )

    previous_token: Mapped["RefreshToken | None"] = relationship(
        back_populates="replaced_by",
        uselist=False,
    )

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(UTC)

    @property
    def is_active(self) -> bool:
        return not self.is_revoked and not self.is_expired

    def revoke(self, replacement: "RefreshToken | None" = None) -> None:
        now = datetime.now(UTC)

        self.revoked_at = now
        self.last_used_at = now

        if replacement is not None:
            self.replaced_by_id = replacement.id

    def mark_used(self) -> None:
        self.last_used_at = datetime.now(UTC)
