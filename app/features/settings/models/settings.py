from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.core.database.helpers import Helper
from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.enums.settings_type import SettingsType


class Settings(Base):
    __tablename__ = "settings"

    code: Mapped[SettingsCode] = mapped_column(
        Helper.enum_column(SettingsCode),
        unique=True,
        nullable=False, )

    string_value: Mapped[str | None]
    int_value: Mapped[int | None]
    bool_value: Mapped[bool | None]

    description: Mapped[str | None]

    value_type: Mapped[SettingsType] = mapped_column(
        Helper.enum_column(SettingsType),
    )
