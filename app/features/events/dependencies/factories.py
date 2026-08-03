from typing import Annotated

from fastapi import Depends

from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.storage.dependencies.services import StorageServiceDep


def get_event_response_factory() -> EventResponseFactory:
    return EventResponseFactory(storage=StorageServiceDep)

def get_activity_type_response_factory() -> ActivityTypeResponseFactory:
    return ActivityTypeResponseFactory(storage=StorageServiceDep)

EventResponseFactoryDep = Annotated[EventResponseFactory, Depends(get_event_response_factory)]
ActivityTypeResponseFactoryDep = Annotated[ActivityTypeResponseFactory, Depends(get_activity_type_response_factory)]