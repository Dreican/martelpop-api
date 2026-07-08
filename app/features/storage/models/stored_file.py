from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.users.models.user import User
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin


class StoredFile(Base, IdMixin, TimestampMixin):
    __tablename__ = "stored_files"

    filename: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    storage_path: Mapped[str] = mapped_column(
        String(500),
        unique=True,
    )

    size: Mapped[int]
    checksum: Mapped[str] = mapped_column(
        String(64),
        unique=True,
    )
    uploaded_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    uploaded_by: Mapped["User"] = relationship(
        foreign_keys=[uploaded_by_id]
    )
