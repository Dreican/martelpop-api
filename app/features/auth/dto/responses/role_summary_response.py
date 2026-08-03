from uuid import UUID

from pydantic import BaseModel

from app.features.auth.enums.role_code import RoleCode


class RoleSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    code: RoleCode
    name: str
