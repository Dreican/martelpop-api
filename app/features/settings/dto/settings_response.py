from pydantic import BaseModel

from app.features.settings.enums.settings_type import SettingsType


class SettingsResponse(BaseModel):
    id: int
    key: str
    value: str | int | bool
    value_type: SettingsType
