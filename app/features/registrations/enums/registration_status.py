from enum import StrEnum


class RegistrationStatus(StrEnum):
    PENDING = "pending"
    REGISTERED = "registered"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"
    EVENT_CANCELLED = "event_cancelled"
