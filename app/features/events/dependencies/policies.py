from typing import Annotated

from fastapi import Depends

from app.features.events.filters.event_access_filter import EventAccessFilter
from app.features.events.policies.event_policy import EventPolicy


def get_event_policy() -> EventPolicy:
    return EventPolicy()


def get_event_access() -> EventAccessFilter:
    return EventAccessFilter()


EventPolicyDep = Annotated[EventPolicy, Depends(get_event_policy)]
EventAccessFilterDep = Annotated[EventAccessFilter, Depends(get_event_access)]
