from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.storage.enums.storage_categories import StorageCategory

if TYPE_CHECKING:
    from app.features.users.models.user import User


class StoredFile(Base):
    __tablename__ = "stored_files"

    filename: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_key: Mapped[str] = mapped_column(String(500), unique=True)
    mime_type: Mapped[str] = mapped_column(String(100))

    size: Mapped[int]
    checksum: Mapped[str] = mapped_column(
        String(64),
        unique=True,
    )

    category: Mapped[StorageCategory] = mapped_column(
        Helper.enum_column(StorageCategory),
        name="storage_category",
        nullable=False,
    )

    uploaded_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id")
    )

    uploaded_by: Mapped["User"] = relationship(
        "User",
        back_populates="uploaded_files",
        foreign_keys=[uploaded_by_id]
    )
