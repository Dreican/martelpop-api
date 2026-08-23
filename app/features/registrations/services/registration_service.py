from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.models.event import Event
from app.features.events.repositories.event_repository import EventRepository
from app.features.registrations.dto.requests.registration_create_request import RegistrationRequest
from app.features.registrations.dto.requests.registration_search_request import RegistrationSearchRequest
from app.features.registrations.dto.requests.registration_update_request import RegistrationUpdateRequest
from app.features.registrations.dto.responses.registration_response import RegistrationResponse
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import (
    RegistrationClosedError,
    EventFullError,
    AlreadyRegisteredError, RegistrationsDisabledError
)
from app.features.registrations.factories.registration_response_factory import RegistrationResponseFactory
from app.features.registrations.factories.registration_summary_response_factory import \
    RegistrationSummaryResponseFactory
from app.features.registrations.models.registration import Registration
from app.features.registrations.policies.registration_policy import RegistrationPolicy
from app.features.registrations.repositories.registration_repository import RegistrationRepository
from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.services.application_settings import ApplicationSettings
from app.features.users.exceptions.user_exceptions import UserInactiveError
from app.features.users.models.user import User
from app.features.users.repositories.user_repository import UserRepository


class RegistrationService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            registration_repository: RegistrationRepository,
            event_repository: EventRepository,
            user_repository: UserRepository,
            registration_policy: RegistrationPolicy,
            registration_response: RegistrationResponseFactory,
            registration_summary_response: RegistrationSummaryResponseFactory,
            application_settings: ApplicationSettings
    ):
        super().__init__(session)
        self._registrations = registration_repository
        self._policy = registration_policy
        self._events = event_repository
        self._users = user_repository
        self._response = registration_response
        self._summary_response = registration_summary_response
        self._settings = application_settings

    async def register_me(
            self,
            event_slug: str,
            request: RegistrationRequest,
            principal: AuthenticatedPrincipal
        ) -> RegistrationResponse:
        event = await self._events.get_for_update_by_slug(event_slug)
        return await self._register(principal.user, event, request, principal)

    async def register_user(
            self,
            event_id: UUID,
            user_id: UUID,
            request: RegistrationRequest,
            principal: AuthenticatedPrincipal
        ) -> RegistrationResponse:
        event = await self._events.get_for_update_by_id(event_id)
        user = await self._users.get_required(user_id)
        return await self._register(user, event, request, principal)


    async def _register(
            self,
            user: User,
            event: Event,
            request: RegistrationRequest,
            principal: AuthenticatedPrincipal
    ):
        registration_settings = await self._settings.registrations()
        if not registration_settings.enabled:
            raise RegistrationsDisabledError(
                settings_code={SettingsCode.REGISTRATIONS_ENABLED},
                value=registration_settings.enabled
            )

        if not user.is_active:
            raise UserInactiveError(user_display_name=user.display_name)

        if user.id == principal.user.id:
            if not self._policy.can_register(event, principal):
                raise PermissionDeniedError(
                    permissions={PermissionCode.REGISTRATION_CREATE},
                    user=principal.user.display_name,
                )
        else:
            if not self._policy.can_manage(event, principal):
                raise PermissionDeniedError(
                    permissions={PermissionCode.REGISTRATION_MANAGE},
                    user=principal.user.display_name,
                )

        if not event.is_registration_open:
            raise RegistrationClosedError(event_slug=event.slug)

        if await self._registrations.exists(event.id, user.id):
            raise AlreadyRegisteredError(
                event_slug=event.slug,
                principal=principal.user.display_name,
                user=user.display_name
            )

        has_capacity = await self._events.has_capacity(
            event.id,
            event.capacity,
        )

        registration = Registration.create(
            event=event,
            user=user,
            note=request.note,
            status=(
                RegistrationStatus.REGISTERED
                if has_capacity
                else RegistrationStatus.WAITLISTED
            ),
            registered_by_id=principal.user.id
        )

        await self._registrations.add(registration)
        await self._save(registration)

        return self._response.create(registration)

    async def cancel(self, registration_id: UUID, principal: AuthenticatedPrincipal) -> RegistrationResponse:
        registration = await self._registrations.get_required(registration_id)

        if not self._policy.can_cancel(registration, principal):
            raise PermissionDeniedError(
                permissions={PermissionCode.REGISTRATION_CANCEL},
                user=principal.user.display_name
            )

        event = await self._events.get_for_update_by_id(
            registration.event_id
        )

        previous_status = registration.status
        registration.cancel(principal.user)

        next_registration = None
        if registration.event.capacity is not None:
            if previous_status is RegistrationStatus.REGISTERED:
                next_registration = await self._registrations.get_next_waitlisted(registration.event_id)

            if next_registration is not None:
                next_registration.promote()

        return await self._persist(registration)

    async def uncancel(self, registration_id: UUID, principal: AuthenticatedPrincipal) -> RegistrationResponse:
        registration = await self._registrations.get_required(registration_id)
        event = await self._events.get_for_update_by_id(
            registration.event_id
        )

        if not event.is_registration_open:
            raise RegistrationClosedError(event_slug=event.slug)

        if not self._policy.can_register(event, principal):
            raise PermissionDeniedError(
                permissions={PermissionCode.REGISTRATION_CANCEL},
                user=principal.user.display_name
            )

        has_capacity = await self._events.has_capacity(
            event.id,
            event.capacity,
        )

        if has_capacity:
            registration.uncancel(principal.user)
        else:
            registration.waitlist(principal.user)

        return await self._persist(registration)

    async def update(
            self,
            registration_id: UUID,
            request: RegistrationUpdateRequest,
            principal: AuthenticatedPrincipal
    ) -> RegistrationResponse:
        registration = await self._registrations.get_required(registration_id)

        if not self._policy.can_update(registration, principal):
            raise PermissionDeniedError(
                permissions={PermissionCode.REGISTRATION_CREATE},
                user=principal.user.display_name
            )

        registration.note = request.note

        return await self._persist(registration)

    async def get_my_registrations(
            self,
            request: RegistrationSearchRequest,
            principal: AuthenticatedPrincipal
    ) -> Page[RegistrationResponse]:
        page = await self._registrations.search_by_user(request, principal.user.id)

        return self._response.create_page(page)

    async def _persist(self, registration: Registration) -> RegistrationResponse:
        await self._commit()
        await self._refresh(registration)

        return self._response.create(registration)
