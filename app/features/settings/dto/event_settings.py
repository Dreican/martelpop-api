from dataclasses import dataclass


@dataclass(frozen=True)
class EventSettings:
    event_location: str
    event_capacity: int
    duration: int
