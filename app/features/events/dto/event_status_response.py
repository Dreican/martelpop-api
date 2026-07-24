from pydantic import BaseModel

from app.features.events.enums.event_status_code import EventStatusCode


class EventStatusResponse(BaseModel):
    model_config = dict(from_attributes=True)
    code: EventStatusCode
    name: str
    description: str | None
    is_default: bool
    sort_order: int
    is_public: bool
    is_bookable: bool
    allow_edit: bool