from typing import Annotated

from fastapi import Depends

from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.factories.activity_type_summary_response_factory import ActivityTypeSummaryResponseFactory
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.events.factories.event_summary_response_factory import EventSummaryResponseFactory
from app.features.events.factories.participant_response_factory import ParticipantResponseFactory
from app.features.registrations.factories.registration_response_factory import RegistrationResponseFactory
from app.features.registrations.factories.registration_summary_response_factory import \
    RegistrationSummaryResponseFactory
from app.features.storage.dependencies.services import StorageServiceDep
from app.features.users.factories.user_response_factory import UserResponseFactory
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory


def get_user_response_factory(storage: StorageServiceDep) -> UserResponseFactory:
    return UserResponseFactory(storage=storage)


def get_user_summary_response_factory(storage: StorageServiceDep) -> UserSummaryResponseFactory:
    return UserSummaryResponseFactory(storage=storage)


UserResponseFactoryDep = Annotated[UserResponseFactory, Depends(get_user_response_factory)]
UserSummaryResponseFactoryDep = Annotated[UserSummaryResponseFactory, Depends(get_user_summary_response_factory)]


def get_activity_type_response_factory(storage: StorageServiceDep) -> ActivityTypeResponseFactory:
    return ActivityTypeResponseFactory(storage=storage)


def get_activity_type_summary_response_factory(storage: StorageServiceDep) -> ActivityTypeSummaryResponseFactory:
    return ActivityTypeSummaryResponseFactory(storage=storage)


ActivityTypeResponseFactoryDep = Annotated[ActivityTypeResponseFactory, Depends(get_activity_type_response_factory)]
ActivityTypeSummaryResponseFactoryDep = Annotated[
    ActivityTypeSummaryResponseFactory, Depends(get_activity_type_summary_response_factory)]


def get_event_response_factory(
        storage: StorageServiceDep,
        activity_type_factory: ActivityTypeResponseFactoryDep,
        user_factory: UserResponseFactoryDep
) -> EventResponseFactory:
    return EventResponseFactory(
        storage=storage,
        activity_type_factory=activity_type_factory,
        user_factory=user_factory
    )


def get_event_summary_response_factory(
        storage: StorageServiceDep,
        activity_type_summary_factory: ActivityTypeSummaryResponseFactoryDep,
) -> EventSummaryResponseFactory:
    return EventSummaryResponseFactory(
        storage=storage,
        activity_type_summary_factory=activity_type_summary_factory,
    )


EventResponseFactoryDep = Annotated[EventResponseFactory, Depends(get_event_response_factory)]
EventSummaryResponseFactoryDep = Annotated[EventSummaryResponseFactory, Depends(get_event_summary_response_factory)]


def get_registration_response_factory(
        storage: StorageServiceDep,
        event_factory: EventSummaryResponseFactoryDep,
        user_factory: UserSummaryResponseFactoryDep
) -> RegistrationResponseFactory:
    return RegistrationResponseFactory(storage=storage, event_factory=event_factory, user_factory=user_factory)


def get_registration_summary_response_factory(
        storage: StorageServiceDep,
) -> RegistrationSummaryResponseFactory:
    return RegistrationSummaryResponseFactory(storage=storage)


def get_participant_response_factory(
        storage: StorageServiceDep,
        event_factory: EventSummaryResponseFactoryDep,
        user_factory: UserSummaryResponseFactoryDep
) -> ParticipantResponseFactory:
    return ParticipantResponseFactory(storage=storage, event_factory=event_factory, user_factory=user_factory)


RegistrationResponseFactoryDep = Annotated[RegistrationResponseFactory, Depends(get_registration_response_factory)]
RegistrationSummaryResponseFactoryDep = Annotated[
    RegistrationSummaryResponseFactory, Depends(get_registration_summary_response_factory)]
ParticipantResponseFactoryDep = Annotated[ParticipantResponseFactory, Depends(get_participant_response_factory)]
