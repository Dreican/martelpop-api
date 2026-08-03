from uuid import UUID

from pydantic import BaseModel

from app.features.events.enums.event_status_code import EventStatusCode


class EventStatusSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    code: EventStatusCode
    name: str

