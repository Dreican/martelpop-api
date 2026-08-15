from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.pagination.page_request import PageRequest
from app.features.events.enums.event_sort import EventSort
from app.features.events.enums.event_status_code import EventStatusCode


class EventSearchRequest(BaseModel):
    pagination: PageRequest = PageRequest()

    query: str | None
    activity_type_id: UUID | None
    starts_after: datetime | None
    ends_before: datetime | None
    statuses: set[EventStatusCode] | None

    sort: EventSort = EventSort.START_DATE_ASC
