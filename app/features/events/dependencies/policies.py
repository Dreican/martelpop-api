from typing import Annotated

from fastapi import Depends

from app.features.events.policies.event_policy import EventPolicy


def get_event_policy() -> EventPolicy:
    return EventPolicy()


EventPolicyDep = Annotated[EventPolicy, Depends(get_event_policy)]