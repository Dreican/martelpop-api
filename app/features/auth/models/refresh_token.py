from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.features.users.models.user import User
from app.shared.database.base import Base
from app.shared.database.mixin import TimestampMixin, IdMixin


class RefreshToken(Base, IdMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped["User"] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    token_hash: Mapped[str] = mapped_column(String(255), unique=True)

    expires_at: Mapped[datetime]
    created_at: Mapped[datetime]
    revoked_at: Mapped[datetime | None]
    replaced_by_id: Mapped[UUID | None] = mapped_column(ForeignKey("refresh_tokens.id"))

    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens",
    )

    replaced_by: Mapped["RefreshToken"] = relationship(
        remote_side=[id],
        uselist=False
    )
