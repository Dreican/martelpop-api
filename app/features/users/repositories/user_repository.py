import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.features.auth.exceptions import EmailAlreadyExistsError
from app.features.users.models.user import User
from app.shared.database.helpers import Helper
from app.shared.database.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[User]):

    async def add(self, user: User) -> None:
        try:
            await super().add(user)
            await self._session.flush()
        except IntegrityError as ex:
            if Helper.is_email_unique_violation(ex):
                logger.debug("Email already exists, unique constraint violation")
                raise EmailAlreadyExistsError() from ex
            raise

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = (
            select(User).where(User.id == user_id)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email_with_identities(self, email: str) -> User | None:
        stmt = (
            select(User).options(selectinload(User.authentication_identities)).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        stmt = (
            select(User).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
