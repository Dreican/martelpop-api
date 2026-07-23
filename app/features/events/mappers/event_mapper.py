from app.features.events.dto.event_response import EventResponse
from app.features.events.mappers.activity_type_mapper import ActivityTypeMapper
from app.features.events.mappers.event_status_mapper import EventStatusMapper
from app.features.events.models.event import Event
from app.features.users.dto.user_response import UserResponse
from app.features.users.mappers.role_mapper import RoleMapper
from app.features.users.mappers.user_mapper import UserMapper
from app.features.users.models.user import User


class EventMapper:

    @staticmethod
    def to_response(event: Event) -> EventResponse:
        return EventResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            slug=event.slug,
            banner_url=(
                f"/files/{event.banner.id}"
                if event.banner
                else None
            ),
            start_date=event.start_at,
            end_date=event.end_at,
            capacity=event.capacity,
            location=event.location,
            activity_type_id=ActivityTypeMapper.to_response(event.activity_type),
            creator=UserMapper.to_response(event.creator),
            status=EventStatusMapper.to_response(event.status)
        )

    @staticmethod
    def to_response_list(users: list[Event]) -> list[EventResponse]:
        return [EventMapper.to_response(user) for user in users]
