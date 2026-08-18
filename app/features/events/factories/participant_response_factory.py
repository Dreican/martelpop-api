from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.participant_response import ParticipantResponse
from app.features.registrations.models.registration import Registration
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory


class ParticipantResponseFactory(ResponseFactory[Registration, ParticipantResponse]):
    def __init__(
            self,
            user_factory: UserSummaryResponseFactory
    ):
        super().__init__()
        self._users = user_factory

    def create(self, entity: Registration) -> ParticipantResponse:
        response = ParticipantResponse.model_validate(entity)

        response.user = self._users.create(entity.user)

        return response
