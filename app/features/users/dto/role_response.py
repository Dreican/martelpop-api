from pydantic import BaseModel


class RoleResponse(BaseModel):
    model_config = dict(from_attributes=True)
    code: str
    name: str
