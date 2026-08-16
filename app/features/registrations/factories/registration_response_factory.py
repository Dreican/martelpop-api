from app.core.factories.response_factory import ResponseFactory
from app.features.events.factories.event_summary_response_factory import EventSummaryResponseFactory
from app.features.registrations.dto.responses.registration_response import RegistrationResponse
from app.features.registrations.models.registration import Registration
from app.features.storage.services.sotrage_service import StorageService
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory


class RegistrationResponseFactory(ResponseFactory[Registration, RegistrationResponse]):
    def __init__(
            self,
            storage: StorageService,
            event_factory: EventSummaryResponseFactory,
            user_factory: UserSummaryResponseFactory
    ):
        super().__init__(storage)
        self._events = event_factory
        self._users = user_factory

    def create(self, entity: Registration) -> RegistrationResponse:
        response = RegistrationResponse.model_validate(entity)

        response.event = self._events.create(entity.event)
        response.user = self._users.create(entity.user)

        return response
