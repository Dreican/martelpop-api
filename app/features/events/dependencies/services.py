from email import policy
from typing import Annotated

from dns.dnssec import Policy
from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.events.dependencies.policies import EventPolicyDep
from app.features.events.dependencies.repositories import (
    EventRepositoryDep,
    ActivityTypeRepositoryDep,
    EventStatusRepositoryDep
)
from app.features.events.services.event_service import EventService


def get_event_service(
        session: SessionDep,
        event_repository: EventRepositoryDep,
        event_status_repository: EventStatusRepositoryDep,
        activity_type_repository: ActivityTypeRepositoryDep,
        slug_service: SlugServiceDep,
        policy_service: EventPolicyDep
) -> EventService:
    return EventService(
        session=session,
        event_repository=event_repository,
        event_status_repository=event_status_repository,
        activity_type_repository=activity_type_repository,
        slug_service=slug_service,
        policy_service=policy_service
    )


EventServiceDep = Annotated[EventService, Depends(get_event_service)]