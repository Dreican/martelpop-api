from datetime import datetime

from pydantic import BaseModel

from app.core.pagination.page_request import PageRequest
from app.features.events.enums.event_sort import EventSort
from app.features.events.enums.event_status_code import EventStatusCode


class EventSearchRequest(BaseModel):
    pagination: PageRequest = PageRequest()

    search: str | None
    activity_type_id: str | None
    starts_after: datetime | None
    ends_before: datetime | None
    statuses: set[EventStatusCode] | None

    page: int = 1
    page_size: int = 20

    sort: EventSort = EventSort.START_DATE_ASC
