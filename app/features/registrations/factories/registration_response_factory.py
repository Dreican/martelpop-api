from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.event_response import EventResponse
from app.features.events.models.event import Event
from app.features.registrations.dto.registration_response import RegistrationResponse
from app.features.registrations.models.registration import Registration
from app.features.storage.services.sotrage_service import StorageService


class RegistrationResponseFactory(ResponseFactory[Registration, RegistrationResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)


    def create(self, entity: Registration) -> RegistrationResponse:
        response = RegistrationResponse.model_validate(entity)

        response.event.banner_url = self._storage.public_url(entity.event.banner_file_id)
        response.user.avatar_url = self._storage.public_url(entity.user.avatar_file_id)

        return response