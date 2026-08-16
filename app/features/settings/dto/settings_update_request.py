from pydantic import BaseModel

from app.features.settings.enums.settings_key import SettingsCode


class SettingsUpdateRequest(BaseModel):
    code: SettingsCode
    value: str | int | bool
