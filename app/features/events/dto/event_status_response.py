from pydantic import BaseModel


class EventStatusResponse(BaseModel):
    model_config = dict(from_attributes=True)
    code: str
    name: str
    description: str | None
    is_default: bool
    sort_order: int
    is_public: bool
    is_bookable: bool
    allow_edit: bool