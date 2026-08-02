from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.enums.event_audience import EventAudience
from app.features.events.models.event import Event
from app.features.registrations.models.registration import Registration
from app.features.users.models.user import User


class RegistrationPolicy:

    def can_view(self, registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        if self._is_owner_or_organizer(registration, principal):
            return True

        if registration.is_cancel:
            return False

        return False


    def can_edit(self, registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return registration.is_owner(principal)


    def can_cancel(self, registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return self._is_owner_or_organizer(registration, principal)

    @staticmethod
    def can_register(event: Event, principal: AuthenticatedPrincipal) -> bool:
        if not event.status.is_bookable:
            return False

        if event.is_full:
            return False

        if event.is_vip_event and not principal.is_vip:
            return False

        return True


    @staticmethod
    def _is_owner_or_organizer(registration: Registration, principal: AuthenticatedPrincipal) -> bool:
        return (principal.is_admin or principal.is_organizer) or registration.is_owner(principal)