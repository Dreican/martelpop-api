from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.events.exceptions.activity_type_exceptions import ActivityTypeNotFoundError
from app.features.events.models.activity_type import ActivityType


class ActivityTypeRepository(SluggableRepository[ActivityType]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=ActivityType, not_found_exception=ActivityTypeNotFoundError)

    async def get_all(self) -> list[ActivityType]:
        stmt = select(ActivityType)
        return list(await self._session.scalars(stmt))