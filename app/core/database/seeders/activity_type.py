from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.events.models.activity_type import ActivityType


async def seed_activity_types(session: AsyncSession) -> None:
    activity_type_seed = (
        {
            "slug": "martelpop",
            "name": "MartelPop",
            "description": "Martel'Pop",
            "is_default": True,
            "default_location": "Maison de Village de Martelange",
            "default_duration_minutes": 240
        },
        {
            "slug": "soiree-jeux-de-societe",
            "name": "Soirée Jeux de Société",
            "description": "Soirée Jeux de Socitété",
            "is_default": False,
            "default_location": "Maison de Village de Martelange",
            "default_duration_minutes": 240
        },
        {
            "slug": "barbecue",
            "name": "Barbecue",
            "description": "Barbecue",
            "is_default": False,
        }
    )

    for data in activity_type_seed:
        exists = await session.scalar(
            select(ActivityType).where(ActivityType.slug == data["slug"])
        )

        if exists is None:
            session.add(ActivityType(**data))
        # else:
        #     exists.name = data["name"]
        #     exists.description = data["description"]
        #     exists.is_default = data["is_default"]
