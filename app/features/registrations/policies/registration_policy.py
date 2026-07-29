from app.features.events.models.event import Event
from app.features.registrations.models.registration import Registration
from app.features.users.models.user import User


class RegistrationPolicy:

    def can_view(self, registration: Registration, user: User | None) -> bool:
        if self._is_owner_or_organizer(registration, user):
            return True

        if registration.is_cancel:
            return False

        return False


    def can_edit(self, registration: Registration, user: User | None) -> bool:
        return self._is_owner_or_organizer(registration, user)


    def can_cancel(self, registration: Registration, user: User | None) -> bool:
        return self._is_owner_or_organizer(registration, user)

    def can_register(self, event: Event, user: User | None) -> bool:
        if not event.status.is_bookable:
            return False

        if event.is_full:
            return False

        if event.is_vip_event and not user.is_vip:
            return False

        return True



    @staticmethod
    def _is_owner_or_organizer(registration: Registration, user: User | None) -> bool:
        return (
            user is not None
            and (
                user.is_admin or user.is_organizer
                or registration.user_id == user.id
            )
        )