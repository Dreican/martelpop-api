from app.features.events.dto.event_status_response import EventStatusResponse
from app.features.events.models.event_status import EventStatus


class EventStatusMapper:

    @staticmethod
    def to_response(event_status: EventStatus) -> EventStatusResponse:
        return EventStatusResponse(
            code=event_status.code,
            name=event_status.name,
            description=event_status.description,
            is_default=event_status.is_default,
            sort_order=event_status.sort_order,
            is_public=event_status.is_public,
            is_bookable=event_status.is_bookable,
            allow_edit=event_status.allow_edit,
        )