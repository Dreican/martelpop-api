from enum import StrEnum


class RegistrationStatus(StrEnum):
    PENDING = "pending"
    REGISTERED = "registered"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"
