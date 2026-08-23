from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.models.event import Event


class EventPolicy:

    def can_view(self, event: Event, principal: Principal) -> bool:

        if event.is_draft:
            if principal.user is None:
                return False

            return (
                    self._is_owner_or_admin(event, principal.require_authenticated())
                    or principal.is_organizer
            )

        match event.audience:
            case EventAudience.PUBLIC:
                return True

            case EventAudience.MEMBERS:
                return principal.user is not None

            case EventAudience.VIP:
                return (
                        principal.user is not None
                        and principal.is_vip
                )

    def can_edit(self, event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                event.status.allow_edit
                and self._is_owner_or_admin(event, principal)
        )

    def can_delete(self, event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                event.status.code is not EventStatusCode.COMPLETED
                and self._is_owner_or_admin(event, principal)
        )

    def can_cancel(self, event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                not event.is_published
                and self._is_owner_or_admin(event, principal)
        )

    def can_complete(self, event: Event, principal: AuthenticatedPrincipal) -> bool:
        return (
                event.is_published
                and self._is_owner_or_admin(event, principal)
        )

    def can_view_participant(self, event: Event, principal: AuthenticatedPrincipal) -> bool:

        if self._is_owner_or_admin(event, principal):
            return True

        match event.audience:
            case EventAudience.VIP:
                return (
                        principal.user is not None
                        and principal.is_vip
                )
            case _:
                return principal.user is not None

    @staticmethod
    def visible_statuses(principal: Principal) -> set[EventStatusCode]:
        if principal.user is None:
            return {
                EventStatusCode.PUBLISHED,
                EventStatusCode.COMPLETED,
            }
        elif principal.is_admin or principal.is_organizer:
            return {
                EventStatusCode.DRAFT,
                EventStatusCode.PUBLISHED,
                EventStatusCode.COMPLETED,
                EventStatusCode.CANCELLED,
            }

        return {
            EventStatusCode.PUBLISHED,
            EventStatusCode.COMPLETED,
            EventStatusCode.CANCELLED,
        }

    @staticmethod
    def visible_audiences(principal: Principal) -> set[EventAudience]:
        if principal.user is None:
            return {
                EventAudience.PUBLIC,
            }
        elif principal.is_admin or principal.is_organizer or principal.is_vip:
            return {
                EventAudience.PUBLIC,
                EventAudience.MEMBERS,
                EventAudience.VIP
            }

        return {
            EventAudience.PUBLIC,
            EventAudience.MEMBERS,
        }

    @staticmethod
    def _is_owner_or_admin(event: Event, principal: AuthenticatedPrincipal) -> bool:
        return principal.is_admin or event.is_owner(principal)
