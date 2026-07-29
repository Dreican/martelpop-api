from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import RegistrationNotFoundError
from app.features.registrations.models.registration import Registration


class RegistrationRepository(BaseRepository[Registration]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Registration, not_found_exception=RegistrationNotFoundError)


    async def get_by_status(self, registration_status: RegistrationStatus) -> list[Registration]:
        stmt = (
            select(Registration).where(Registration.status == registration_status)
        )

        return list(await self._session.scalars(stmt))