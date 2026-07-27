from app.features.auth.enums.role_code import RoleCode
from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.models.event import Event
from app.features.events.models.event_status import EventStatus
from app.features.users.models.user import User


class EventPolicy:

    def can_view(self, event: Event, user: User | None) -> bool:
        if event.is_draft:
            return (
                self._is_owner_or_admin(event, user)
                or (
                    user is not None
                    and user.role.code == RoleCode.ORGANIZER
                )
            )

        if event.audience == EventAudience.PUBLIC:
            return True

        if event.audience == EventAudience.VIP:
            return (
                user is not None
                and user.is_vip
            )

        return False


    def can_edit(self, event: Event, user: User | None) -> bool:
        return (
            event.status.allow_edit
            and self._is_owner_or_admin(event, user)
        )

    def can_cancel(self, event: Event, user: User | None) -> bool:
        return (
            not event.is_published
            and self._is_owner_or_admin(event, user)
        )

    def can_complete(self, event: Event, user: User | None) -> bool:
        return (
            event.is_published
            and self._is_owner_or_admin(event, user)
        )

    @staticmethod
    def visible_statuses(user: User | None) -> set[EventStatusCode]:
        if user is None:
            return {
               EventStatusCode.PUBLISHED,
               EventStatusCode.COMPLETED,
            }
        elif user.is_admin or user.is_organizer:
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
    def visible_audiences(user: User | None) -> set[EventAudience]:
        if user is None:
            return {
                EventAudience.PUBLIC,
            }
        elif user.is_admin or user.is_organizer:
            return {
                EventAudience.PUBLIC,
                EventAudience.MEMBERS,
                EventAudience.VIP,
                EventAudience.ORGANIZER
            }
        elif user.is_vip:
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
    def _is_owner_or_admin(event: Event, user: User | None) -> bool:
        return (
            user is not None
            and (
                user.is_admin
                or event.created_by == user.id
            )
        )