from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import EventResponseFactoryDep, ParticipantResponseFactoryDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.events.dependencies.policies import EventPolicyDep, EventAccessFilterDep
from app.features.events.dependencies.repositories import (
    EventRepositoryDep,
    ActivityTypeRepositoryDep,
    EventStatusRepositoryDep
)
from app.features.events.services.event_service import EventService
from app.features.registrations.dependencies.repositories import RegistrationRepositoryDep
from app.features.settings.dependencies.settings import ApplicationSettingsDep


def get_event_service(
        session: SessionDep,
        event_repository: EventRepositoryDep,
        event_status_repository: EventStatusRepositoryDep,
        activity_type_repository: ActivityTypeRepositoryDep,
        registrations_repository: RegistrationRepositoryDep,
        slug_service: SlugServiceDep,
        policy_service: EventPolicyDep,
        access_service: EventAccessFilterDep,
        application_settings: ApplicationSettingsDep,
        response_factory: EventResponseFactoryDep,
        participant_response: ParticipantResponseFactoryDep

) -> EventService:
    return EventService(
        session=session,
        event_repository=event_repository,
        event_status_repository=event_status_repository,
        activity_type_repository=activity_type_repository,
        registrations_repository=registrations_repository,
        slug_service=slug_service,
        event_policy=policy_service,
        event_access=access_service,
        application_settings=application_settings,
        event_response=response_factory,
        participant_response=participant_response
    )


EventServiceDep = Annotated[EventService, Depends(get_event_service)]
