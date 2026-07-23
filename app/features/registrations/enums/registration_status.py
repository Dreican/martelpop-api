from enum import StrEnum


class RegistrationStatus(StrEnum):
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    WAITLISTED = "WAITLISTED"
