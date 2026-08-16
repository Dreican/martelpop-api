from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.models.event_status import EventStatus


async def seed_event_status(session: AsyncSession) -> None:
    event_status_seed = (
        {
            "code": EventStatusCode.DRAFT,
            "name": "Draft",
            "description": "Event is in draft state",
            "is_default": True
        },
        {
            "code": EventStatusCode.PUBLISHED,
            "name": "Published",
            "description": "Event is published",
            "is_default": False
        },
        {
            "code": EventStatusCode.CANCELLED,
            "name": "Cancelled",
            "description": "Event is cancelled",
            "is_default": False
        },
        {
            "code": EventStatusCode.COMPLETED,
            "name": "Completed",
            "description": "Event is completed",
            "is_default": False
        },
    )

    for data in event_status_seed:
        exists = await session.scalar(
            select(EventStatus).where(EventStatus.code == data["code"])
        )

        if exists is None:
            session.add(EventStatus(**data))
        # else:
        #     exists.name = data["name"]
        #     exists.description = data["description"]
        #     exists.is_default = data["is_default"]
