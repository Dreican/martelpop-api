from dataclasses import dataclass
from typing import Collection
from uuid import UUID

from app.features.events.enums.event_audience import EventAudience
from app.features.events.models.event_status import EventStatus


@dataclass(frozen=True)
class EventAccess:
    statuses: tuple[EventStatus]
    audiences: tuple[EventAudience]

    creator_id: UUID | None = None
    activity_type_id: UUID | None = None

    include_deleted: bool = False

    @property
    def restrict_to_creator(self) -> bool:
        return self.creator_id is not None

    @property
    def can_view_deleted(self) -> bool:
        return self.include_deleted