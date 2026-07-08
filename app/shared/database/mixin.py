from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import DateTime, func, ForeignKey, UUID, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


class AuditMixin:
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )
