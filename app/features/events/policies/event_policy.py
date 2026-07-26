from app.features.auth.enums.role_code import RoleCode
from app.features.events.enums.event_audience import EventAudience
from app.features.events.models.event import Event
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

    def can_publish(self, event: Event, user: User | None) -> bool:
        return (
            event.is_draft
            and self._is_owner_or_admin(event, user)
        )

    def can_unpublish(self, event: Event, user: User | None) -> bool:
        return (
            (event.is_published
            or event.is_cancelled)
            and self._is_owner_or_admin(event, user)
        )

    def can_cancel(self, event: Event, user: User | None) -> bool:
        return (
            not event.is_published
            and self._is_owner_or_admin(event, user)
        )

    def visible_audiences(self, user: User | None) -> list[EventAudience]:
        if user is None:
            return [
                EventAudience.PUBLIC,
            ]
        elif user.is_admin or user.is_organizer:
            return [
                EventAudience.PUBLIC,
                EventAudience.MEMBERS,
                EventAudience.VIP,
                EventAudience.ORGANIZER
            ]
        elif user.is_vip:
            return [
                EventAudience.PUBLIC,
                EventAudience.MEMBERS,
                EventAudience.VIP
            ]

        return [
            EventAudience.PUBLIC,
            EventAudience.MEMBERS,
        ]


    @staticmethod
    def _is_owner_or_admin(event: Event, user: User | None) -> bool:
        return (
            user is not None
            and (
                user.is_admin
                or event.created_by == user.id
            )
        )