from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base


class Settings(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(255), unique=True)
    string_value: Mapped[str | None]
    int_value: Mapped[int | None]
    bool_value: Mapped[bool | None]