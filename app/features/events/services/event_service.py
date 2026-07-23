from app.features.events.repositories.event_repository import EventRepository


class EventService:
    def __init__(
            self,
            event_repository: EventRepository
    ):
        self.event = event_repository
