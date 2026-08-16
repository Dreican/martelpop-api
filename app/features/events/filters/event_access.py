from dataclasses import dataclass
from typing import Collection
from uuid import UUID

from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_status_code import EventStatusCode


@dataclass(frozen=True)
class EventAccess:
    statuses: tuple[EventStatusCode, ...]
    audiences: tuple[EventAudience, ...]

    creator_id: UUID | None = None
    activity_type_id: UUID | None = None

    include_deleted: bool = False

    @property
    def restrict_to_creator(self) -> bool:
        return self.creator_id is not None

    @property
    def can_view_deleted(self) -> bool:
        return self.include_deleted

    def allowed_statuses(self, requested: Collection[EventStatusCode] | None) -> set[EventStatusCode]:
        statuses = set(self.statuses)

        if requested:
            statuses = statuses.intersection(requested)

        return statuses
