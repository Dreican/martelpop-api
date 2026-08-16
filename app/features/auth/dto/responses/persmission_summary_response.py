from pydantic import BaseModel

from app.features.auth.enums.permission_code import PermissionCode


class PermissionSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    code: PermissionCode
    name: str
