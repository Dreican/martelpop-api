from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None]


class AuditMixin:
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )
