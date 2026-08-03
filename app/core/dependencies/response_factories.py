from typing import Annotated

from fastapi import Depends

from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.registrations.factories.registration_response_factory import RegistrationResponseFactory
from app.features.storage.dependencies.services import StorageServiceDep
from app.features.users.factories.user_response_factory import UserResponseFactory


def get_user_response_factory(storage: StorageServiceDep) -> UserResponseFactory:
    return UserResponseFactory(storage=storage)


UserResponseFactoryDep = Annotated[UserResponseFactory, Depends(get_user_response_factory)]


def get_activity_type_response_factory(storage: StorageServiceDep) -> ActivityTypeResponseFactory:
    return ActivityTypeResponseFactory(storage=storage)


ActivityTypeResponseFactoryDep = Annotated[ActivityTypeResponseFactory, Depends(get_activity_type_response_factory)]


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


EventResponseFactoryDep = Annotated[EventResponseFactory, Depends(get_event_response_factory)]


def get_registration_response_factory(
        storage: StorageServiceDep,
        event_factory: EventResponseFactoryDep,
        user_factory: UserResponseFactoryDep
) -> RegistrationResponseFactory:
    return RegistrationResponseFactory(storage=storage, event_factory=event_factory, user_factory=user_factory)


RegistrationResponseFactoryDep = Annotated[RegistrationResponseFactory, Depends(get_registration_response_factory)]
