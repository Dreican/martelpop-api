from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_events: int

    published_events: int

    registrations: int

    upcoming_events: int

    users: int
