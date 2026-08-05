from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import EventResponseFactoryDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.events.dependencies.policies import EventPolicyDep, EventAccessFilterDep
from app.features.events.dependencies.repositories import (
    EventRepositoryDep,
    ActivityTypeRepositoryDep,
    EventStatusRepositoryDep
)
from app.features.events.services.event_service import EventService
from app.features.settings.dependencies.settings import ApplicationSettingsDep


def get_event_service(
        session: SessionDep,
        event_repository: EventRepositoryDep,
        event_status_repository: EventStatusRepositoryDep,
        activity_type_repository: ActivityTypeRepositoryDep,
        slug_service: SlugServiceDep,
        policy_service: EventPolicyDep,
        access_service: EventAccessFilterDep,
        response_factory: EventResponseFactoryDep,
        application_settings: ApplicationSettingsDep
) -> EventService:
    return EventService(
        session=session,
        event_repository=event_repository,
        event_status_repository=event_status_repository,
        activity_type_repository=activity_type_repository,
        slug_service=slug_service,
        event_policy=policy_service,
        event_access=access_service,
        event_response=response_factory,
        application_settings=application_settings
    )


EventServiceDep = Annotated[EventService, Depends(get_event_service)]
