from app.features.events.dto.responses.event_summary_response import EventSummaryResponse
from app.features.registrations.dto.responses.registration_summary_response import RegistrationSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class RegistrationResponse(RegistrationSummaryResponse):
    event: EventSummaryResponse
    user: UserSummaryResponse
    note: str