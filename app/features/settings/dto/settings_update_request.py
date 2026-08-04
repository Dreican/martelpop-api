from pydantic import BaseModel

class SettingsUpdateRequest(BaseModel):
    key: str
    string_value: str | None
    int_value: int | None
    bool_value: bool | None