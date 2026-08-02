from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_service import BaseService
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.models.event import Event
from app.features.events.repositories.event_repository import EventRepository
from app.features.registrations.dto.registration_request import RegistrationRequest
from app.features.registrations.dto.registration_response import RegistrationResponse
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import RegistrationNotFoundError
from app.features.registrations.mappers.registration_mapper import RegistrationMapper
from app.features.registrations.models import registration
from app.features.registrations.models.registration import Registration
from app.features.registrations.policies.registration_policy import RegistrationPolicy
from app.features.registrations.repositories.registration_repository import RegistrationRepository


class RegistrationService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            registration_repository: RegistrationRepository,
            registration_policy: RegistrationPolicy,
            event_repository: EventRepository,
    ):
        super().__init__(session)
        self._repository = registration_repository
        self._policy = registration_policy
        self._event = event_repository

    async def register(self, request: RegistrationRequest, principal: AuthenticatedPrincipal):
        event = await self._event.get_required(request.event_id)

        if not self._policy.can_register(event, principal):
            raise RegistrationNotFoundError(event_slug=event.slug)

        new_registration = Registration(
            event=event,
            note=request.note,
            user_id=principal.user.id,
            status=RegistrationStatus.REGISTERED
        )
        await self._repository.add(new_registration)
        await self._flush()
        await self._refresh(event)

        return RegistrationMapper.to_response(new_registration)


