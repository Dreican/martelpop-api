from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query, Depends

from app.core.pagination.page_request import PageRequest
from app.features.events.dto.requests.event_search_request import EventSearchRequest
from app.features.events.enums.event_sort import EventSort
from app.features.events.enums.event_status_code import EventStatusCode


async def get_event_search_request(
        page: int = Query(1),
        page_size: int = Query(20),
        query: str | None = Query(None),
        activity_type_id: UUID | None = Query(None),
        starts_after: datetime | None = Query(None),
        ends_before: datetime | None = Query(None),
        statuses: set[EventStatusCode] | None = Query(None),
        sort: EventSort = Query(EventSort.START_DATE_ASC),
) -> EventSearchRequest:
    return EventSearchRequest(
        pagination=PageRequest(
            page=page,
            page_size=page_size,
        ),
        query=query,
        activity_type_id=activity_type_id,
        starts_after=starts_after,
        ends_before=ends_before,
        statuses=statuses,
        sort=sort,
    )


EventSearchRequestDep = Annotated[EventSearchRequest, Depends(get_event_search_request)]
