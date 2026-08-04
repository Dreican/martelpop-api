from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.settings.enums.settings_type import SettingsType


class Settings(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(255), unique=True)
    string_value: Mapped[str | None]
    int_value: Mapped[int | None]
    bool_value: Mapped[bool | None]
    value_type: Mapped[SettingsType] = mapped_column(
        Helper.enum_column(SettingsType),
    )