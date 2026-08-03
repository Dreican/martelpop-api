from app.features.events.mappers.event_mapper import EventMapper
from app.features.registrations.dto.registration_response import RegistrationResponse
from app.features.registrations.models.registration import Registration
from app.features.users.mappers.user_mapper import UserMapper


class RegistrationMapper:
    @staticmethod
    def to_response(registration: Registration) -> RegistrationResponse:
        return RegistrationResponse(
            id=registration.id,
            event=EventMapper.to_response(registration.event),
            user=UserMapper.to_response(registration.user),
            status=registration.status,
            note=registration.note
        )

    @staticmethod
    def to_response_list(registrations: list[Registration]) -> list[RegistrationResponse]:
        return [RegistrationMapper.to_response(registration) for registration in registrations]