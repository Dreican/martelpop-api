from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

if TYPE_CHECKING:
    from app.features.users.models.user import User


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None]

    deleted_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    if TYPE_CHECKING:
        deleted_by: Mapped["User | None"]
    else:
        @declared_attr
        def deleted_by(cls) -> Mapped["User | None"]:
            return relationship(
                "User",
                foreign_keys=[cls.deleted_by_id],
            )
