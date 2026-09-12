from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import (
    EventResponseFactoryDep, ParticipantResponseFactoryDep,
    StoredFileResponseFactoryDep, ActivityTypeAdminResponseFactoryDep, ActivityTypeSummaryResponseFactoryDep,
    ActivityTypeResponseFactoryDep
)
from app.core.dependencies.slug import SlugServiceDep
from app.features.events.dependencies.policies import EventPolicyDep, EventAccessFilterDep
from app.features.events.dependencies.repositories import (
    EventRepositoryDep,
    ActivityTypeRepositoryDep,
    EventStatusRepositoryDep
)
from app.features.events.services.activity_type_service import ActivityTypeService
from app.features.events.services.event_service import EventService
from app.features.registrations.dependencies.repositories import RegistrationRepositoryDep
from app.features.settings.dependencies.settings import ApplicationSettingsDep
from app.features.storage.dependencies.services import FileServiceDep


def get_event_service(
        session: SessionDep,
        event_repository: EventRepositoryDep,
        event_status_repository: EventStatusRepositoryDep,
        activity_type_repository: ActivityTypeRepositoryDep,
        registrations_repository: RegistrationRepositoryDep,
        slug_service: SlugServiceDep,
        file_service: FileServiceDep,
        policy_service: EventPolicyDep,
        access_service: EventAccessFilterDep,
        application_settings: ApplicationSettingsDep,
        response_factory: EventResponseFactoryDep,
        participant_response: ParticipantResponseFactoryDep,
        store_file_response: StoredFileResponseFactoryDep

) -> EventService:
    return EventService(
        session=session,
        event_repository=event_repository,
        event_status_repository=event_status_repository,
        activity_type_repository=activity_type_repository,
        registrations_repository=registrations_repository,
        slug_service=slug_service,
        file_service=file_service,
        event_policy=policy_service,
        event_access=access_service,
        application_settings=application_settings,
        event_response=response_factory,
        participant_response=participant_response,
        stored_file_response=store_file_response
    )


EventServiceDep = Annotated[EventService, Depends(get_event_service)]


def get_activity_type_service(
        session: SessionDep,
        activity_type_repository: ActivityTypeRepositoryDep,
        slug_service: SlugServiceDep,
        file_service: FileServiceDep,
        application_settings: ApplicationSettingsDep,
        stored_file_response: StoredFileResponseFactoryDep,
        response_summary_factory: ActivityTypeSummaryResponseFactoryDep,
        response_factory: ActivityTypeResponseFactoryDep,
        response_admin_factory: ActivityTypeAdminResponseFactoryDep,
) -> ActivityTypeService:
    return ActivityTypeService(
        session=session,
        activity_type_repository=activity_type_repository,
        slug_service=slug_service,
        file_service=file_service,
        application_settings=application_settings,
        stored_file_response=stored_file_response,
        response_factory=response_factory,
        response_summary_factory=response_summary_factory,
        response_admin_factory=response_admin_factory,
    )


ActivityTypeServiceDep = Annotated[ActivityTypeService, Depends(get_activity_type_service)]
