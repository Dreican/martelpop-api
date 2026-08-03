from app.core.factories.response_factory import ResponseFactory
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.registrations.dto.registration_response import RegistrationResponse
from app.features.registrations.models.registration import Registration
from app.features.storage.services.sotrage_service import StorageService
from app.features.users.factories.user_response_factory import UserResponseFactory


class RegistrationResponseFactory(ResponseFactory[Registration, RegistrationResponse]):
    def __init__(
            self,
            storage: StorageService,
            event_factory: EventResponseFactory,
            user_factory: UserResponseFactory
    ):
        super().__init__(storage)
        self._events = event_factory
        self._users = user_factory

    def create(self, entity: Registration) -> RegistrationResponse:
        response = RegistrationResponse.model_validate(entity)

        response.event = self._events.create(entity.event)
        response.user = self._users.create(entity.user)

        return response
