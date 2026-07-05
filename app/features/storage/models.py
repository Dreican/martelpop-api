from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    pass


class StoredFile(Base, IdMixin, TimestampMixin):
    __tablename__ = "stored_files"

    filename: Mapped[str] = mapped_column(String(255), Unique=True, nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    size: Mapped[int]
    checksum: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
