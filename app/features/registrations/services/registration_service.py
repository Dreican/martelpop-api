from app.features.registrations.factories.registration_mapper import RegistrationMapper
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.repositories.event_repository import EventRepository
from app.features.registrations.dto.cancel_request import CancelRequest
from app.features.registrations.dto.registration_create_request import RegistrationRequest
from app.features.registrations.dto.registration_response import RegistrationResponse
from app.features.registrations.dto.registration_search_request import RegistrationSearchRequest
from app.features.registrations.dto.registration_update_request import RegistrationUpdateRequest
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import RegistrationClosedError, EventFullError, \
    AlreadyRegisteredError
from app.features.registrations.factories.registration_response_factory import RegistrationResponseFactory
from app.features.registrations.models.registration import Registration
from app.features.registrations.policies.registration_policy import RegistrationPolicy
from app.features.registrations.repositories.registration_repository import RegistrationRepository


class RegistrationService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            registration_repository: RegistrationRepository,
            event_repository: EventRepository,
            registration_policy: RegistrationPolicy,
            registration_response: RegistrationResponseFactory
    ):
        super().__init__(session)
        self._registrations = registration_repository
        self._policy = registration_policy
        self._events = event_repository
        self._response = registration_response

    async def register(self, request: RegistrationRequest, principal: AuthenticatedPrincipal) -> RegistrationResponse:
        event = await self._events.get_required(request.event_id)

        if event.is_full:
            raise EventFullError(event_slug=event.slug)

        if not event.is_registration_open:
            raise RegistrationClosedError(event_slug=event.slug)

        if await self._registrations.exists(event.id, principal.user.id):
            raise AlreadyRegisteredError(event_slug=event.slug, user_display_name=principal.user.display_name)

        if not self._policy.can_register(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.REGISTRATION_CREATE},
                                        user=principal.user.display_name)

        registration = Registration(
            event=event,
            user=principal.user,
            note=request.note,
            status=RegistrationStatus.REGISTERED
        )
        await self._registrations.add(registration)
        await self._save(registration)

        return self._response.create(registration)

    async def cancel(self, request: CancelRequest, principal: AuthenticatedPrincipal) -> RegistrationResponse:
        registration = await self._registrations.get_required(request.registration_id)

        if not self._policy.can_cancel(registration, principal):
            raise PermissionDeniedError(
                permissions={PermissionCode.REGISTRATION_CANCEL},
                user=principal.user.display_name
            )

        registration.cancel()

        return await self._persist(registration)

    async def update(self, request: RegistrationUpdateRequest, principal: AuthenticatedPrincipal) -> RegistrationResponse:
        registration = await self._registrations.get_required(request.registration_id)

        if not self._policy.can_update(registration, principal):
            raise PermissionDeniedError(
                permissions={PermissionCode.REGISTRATION_CREATE},
                user=principal.user.display_name
            )

        registration.note = request.note

        return await self._persist(registration)

    async def get_my_registrations(self, request: RegistrationSearchRequest, principal: AuthenticatedPrincipal) -> Page[RegistrationResponse]:
        page = await self._registrations.search_by_user(request, principal.user.id)

        return self._response.create_page(page)


    async def _persist(self, registration: Registration) -> RegistrationResponse:
        await self._commit()
        await self._refresh(registration)

        return self._response.create(registration)
