import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.helpers import Helper
from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.auth.exceptions.authentication_exceptions import EmailAlreadyExistsError
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class UserRepository(SluggableRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User)

    async def add(self, entity: User) -> None:
        try:
            await super().add(entity)
            await self._session.flush()
        except IntegrityError as ex:
            if Helper.is_email_unique_violation(ex):
                logger.debug("Email already exists, unique constraint violation")
                raise EmailAlreadyExistsError() from ex
            raise

    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User).where(User.email == email)
        )

        return await self._session.scalar(stmt)

    async def get_by_email_with_identities(self, email: str) -> User | None:
        stmt = (
            select(User).options(selectinload(User.authentication_identities)).where(User.email == email)
        )

        return await self._session.scalar(stmt)

    async def exists_by_email(self, email: str) -> bool:
        stmt = (
            select(User).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
