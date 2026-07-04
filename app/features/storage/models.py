import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func, BigInteger
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.features.user.models import User
    from app.features.registrations.models import Registration


class StoredFile(Base, TimestampMixin):
    __tablename__ = "stored_files"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), Unique=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    storage_path: Mapped[str] = mapped_column(String(500))
    size: Mapped[int]
    checksum: Mapped[str] = mapped_column(String(64), unique=True)