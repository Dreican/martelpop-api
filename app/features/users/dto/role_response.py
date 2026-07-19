from uuid import UUID

from pydantic import BaseModel


class RoleResponse(BaseModel):
    code: str
    name: str
