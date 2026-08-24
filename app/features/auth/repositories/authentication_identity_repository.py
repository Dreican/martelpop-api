from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.exceptions.authentication_exceptions import AuthenticationIdentityNotFoundError
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.users.models.user import User


class AuthenticationIdentityRepository(BaseRepository[AuthenticationIdentity]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=AuthenticationIdentity, not_found_exception=AuthenticationIdentityNotFoundError)

    async def get_by_id(self, entity_id: UUID) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .options(selectinload(AuthenticationIdentity.user))
            .where(AuthenticationIdentity.id == entity_id)
        )
        return await self._session.scalar(stmt)

    async def get_by_provider(self, provider: AuthProvider, provider_subject: str) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .options(selectinload(AuthenticationIdentity.user))
            .where(
                AuthenticationIdentity.provider == provider,
                AuthenticationIdentity.provider_user_id == provider_subject
            )
        )
        return await self._session.scalar(stmt)

    async def get_by_user_id(self, user_id: UUID) -> list[AuthenticationIdentity]:
        stmt = (
            select(AuthenticationIdentity)
            .where(AuthenticationIdentity.user_id == user_id)
        )
        return list(await self._session.scalars(stmt))

    async def get_by_user_email(self, email: str) -> AuthenticationIdentity | None:
        stmt = (
            select(AuthenticationIdentity)
            .join(AuthenticationIdentity.user)
            .options(
                selectinload(AuthenticationIdentity.user)
                .selectinload(User.role)
            )
            .where(
                AuthenticationIdentity.provider == AuthProvider.LOCAL,
                User.email == email
            )
        )
        return await self._session.scalar(stmt)
