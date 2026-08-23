from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.models.event import Event
from app.features.registrations.models.registration import Registration


class RegistrationPolicy:

    def can_view(self, registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        if self._is_owner_or_organizer(registration, principal):
            return True

        if registration.is_cancelled:
            return False

        return True

    def can_cancel(self, registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return (
                not registration.is_cancelled
                and self._is_owner_or_organizer(registration, principal)
        )

    @staticmethod
    def can_update(registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return registration.is_owner(principal)

    @staticmethod
    def can_manage(event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                principal.is_admin
                or principal.is_organizer
                or event.is_owner(principal)
        )

    @staticmethod
    def can_register(event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                event.status.code == EventStatusCode.PUBLISHED
                and (
                    not event.is_vip_event
                    or principal.is_vip
                )
        )

    @staticmethod
    def _is_owner_or_organizer(registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return (
                principal.is_admin
                or principal.is_organizer
                or registration.is_owner(principal)
        )
