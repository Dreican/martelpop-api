from uuid import UUID

from pydantic import BaseModel


class RoleResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    code: str
    name: str
    description: str
    is_default: bool

    # permissions: list[PermissionResponse]
