from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.models.refresh_token import RefreshToken
from app.features.users.models.user import User
from app.shared.database.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        stmt = (
            select(RefreshToken).where(RefreshToken.jti == jti)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_token_hash(self, token_hash: str):
        stmt = (
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )

        result = await self._session.scalar(stmt)
        return result

    async def get_active_by_user(self, user_id: UUID) -> list[RefreshToken]:
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > datetime.now(UTC),
            )
        )

        result = await self._session.scalars(stmt)
        return list(result)

    async def revoke(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoke()

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=datetime.now(UTC))
        )

        result = await self._session.execute(stmt)
        refresh_tokens = result.scalars().all()

        for refresh_token in refresh_tokens:
            refresh_token.revoke()

    async def delete_expired(self) -> None:
        stmt = (
            select(RefreshToken).where(RefreshToken.expires_at < datetime.now(UTC))
        )

        result = await self._session.execute(stmt)
        refresh_tokens = result.scalars().all()

        for refresh_token in refresh_tokens:
           await self.delete(refresh_token).where