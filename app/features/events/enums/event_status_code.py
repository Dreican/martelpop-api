from enum import StrEnum


class EventStatusCode(StrEnum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
