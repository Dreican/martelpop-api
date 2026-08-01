from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.events.repositories.activity_type_repository import ActivityTypeRepository
from app.features.events.repositories.event_repository import EventRepository
from app.features.events.repositories.event_status_repository import EventStatusRepository


def get_event_repository(session: SessionDep) -> EventRepository:
    return EventRepository(session=session)


def get_activity_type_repository(session: SessionDep) -> ActivityTypeRepository:
    return ActivityTypeRepository(session=session)


def get_event_status_repository(session: SessionDep) -> EventStatusRepository:
    return EventStatusRepository(session=session)

EventRepositoryDep = Annotated[EventRepository, Depends(get_event_repository)]
ActivityTypeRepositoryDep = Annotated[ActivityTypeRepository, Depends(get_activity_type_repository)]
EventStatusRepositoryDep = Annotated[EventStatusRepository, Depends(get_event_status_repository)]
