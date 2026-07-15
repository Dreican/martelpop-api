from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.users.models.user import User
from app.shared.database.repositories.base_repository import BaseRepository


class AuthenticationIdentityRepository(BaseRepository[AuthenticationIdentity]):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, identity_id: UUID) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .options(selectinload(AuthenticationIdentity.user))
            .where(AuthenticationIdentity.id == identity_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_provider(self, provider: AuthProvider, provider_subject: str) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .options(selectinload(AuthenticationIdentity.user))
            .where(
                AuthenticationIdentity.provider == provider,
                AuthenticationIdentity.provider_subject == provider_subject)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> list[AuthenticationIdentity]:
        stmt = (
            select(AuthenticationIdentity)
            .where(AuthenticationIdentity.user_id == user_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user_email(self, email: str) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .join(AuthenticationIdentity.user)
            .options(selectinload(AuthenticationIdentity.user))
            .where(
                AuthenticationIdentity.provider == AuthProvider.LOCAL,
                User.email == email
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
