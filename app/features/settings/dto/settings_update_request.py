from pydantic import BaseModel

class SettingsUpdateRequest(BaseModel):
    key: str
    value: str | int | bool
