from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.users.models.user import User
from app.shared.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

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
            select(User).options(selectinload(User.auth_identities)).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        stmt = (
            select(User).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

