from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.event_summary_response import EventSummaryResponse
from app.features.events.factories.activity_type_summary_response_factory import ActivityTypeSummaryResponseFactory
from app.features.events.models.event import Event


class EventSummaryResponseFactory(ResponseFactory[Event, EventSummaryResponse]):
    def __init__(
            self,
            activity_type_summary_factory: ActivityTypeSummaryResponseFactory
    ):
        super().__init__()
        self._activity_type = activity_type_summary_factory

    def create(self, entity: Event) -> EventSummaryResponse:
        response = EventSummaryResponse.model_validate(entity)

        response.banner_url = self.file_url(entity.banner_file_id)
        response.activity_type = self._activity_type.create(entity.activity_type)

        return response
