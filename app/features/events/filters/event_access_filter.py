from app.features.auth.security.principal import Principal
from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.filters.event_access import EventAccess


class EventAccessFilter:

    def build(self, principal: Principal) -> EventAccess:
        if principal.user is None:
            return EventAccess(
                statuses=(
                    EventStatusCode.PUBLISHED,
                    EventStatusCode.COMPLETED
                ),
                audiences=(
                    EventAudience.PUBLIC,
                ),
            )

        if principal.is_admin:
            return EventAccess(
                statuses=(
                    EventStatusCode.DRAFT,
                    EventStatusCode.PUBLISHED,
                    EventStatusCode.COMPLETED,
                    EventStatusCode.CANCELLED,
                ),
                audiences=(
                    EventAudience.PUBLIC,
                    EventAudience.MEMBERS,
                    EventAudience.VIP,
                ),
            )

        if principal.is_organizer:
            return EventAccess(
                statuses=(
                    EventStatusCode.DRAFT,
                    EventStatusCode.PUBLISHED,
                    EventStatusCode.COMPLETED,
                    EventStatusCode.CANCELLED,
                ),
                audiences=(
                    EventAudience.PUBLIC,
                    EventAudience.MEMBERS,
                    EventAudience.VIP,
                ),
            )

        if principal.is_vip:
            return EventAccess(
                statuses=(
                    EventStatusCode.PUBLISHED,
                    EventStatusCode.COMPLETED,
                    EventStatusCode.CANCELLED,
                ),
                audiences=(
                    EventAudience.PUBLIC,
                    EventAudience.MEMBERS,
                    EventAudience.VIP,
                ),
            )

        return EventAccess(
            statuses=(
                EventStatusCode.PUBLISHED,
                EventStatusCode.COMPLETED,
                EventStatusCode.CANCELLED,
            ),
            audiences=(
                EventAudience.PUBLIC,
                EventAudience.MEMBERS,
            ),
        )
