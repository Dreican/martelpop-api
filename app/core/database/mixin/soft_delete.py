from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.users.models.user import User


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None]
    deleted_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )
    deleted_by: Mapped["User"] = relationship(
        foreign_keys=[deleted_by_id],
    )
