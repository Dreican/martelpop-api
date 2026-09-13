from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.event_admin_response import EventAdminResponse
from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.models.event import Event
from app.features.users.factories.user_response_factory import UserResponseFactory


class EventResponseFactory(ResponseFactory[Event, EventAdminResponse]):
    def __init__(
            self,
            activity_type_factory: ActivityTypeResponseFactory,
            user_factory: UserResponseFactory
    ):
        super().__init__()
        self._activity_type_factory = activity_type_factory
        self._users = user_factory

    def create(self, entity: Event) -> EventAdminResponse:
        response: EventAdminResponse = super().create(entity)

        response.banner_url = self.file_url(entity.banner_file_id)
        response.activity_type = self._activity_type_factory.create(entity.activity_type)
        response.creator = self._users.create(entity.creator)

        if entity.deleted_by is not None:
            response.deleted_by = self._users.create(entity.deleted_by)

        return response
