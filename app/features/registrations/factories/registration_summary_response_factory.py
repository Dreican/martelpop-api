from app.core.factories.response_factory import ResponseFactory
from app.features.registrations.dto.responses.registration_summary_response import RegistrationSummaryResponse
from app.features.registrations.models.registration import Registration
from app.features.storage.services.sotrage_service import StorageService


class RegistrationSummaryResponseFactory(ResponseFactory[Registration, RegistrationSummaryResponse]):
    def __init__(
            self,
            storage: StorageService
    ):
        super().__init__(storage)

    def create(self, entity: Registration) -> RegistrationSummaryResponse:
        response = RegistrationSummaryResponse.model_validate(entity)

        return response
