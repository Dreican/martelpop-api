from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.models.refresh_token import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        stmt = (
            select(RefreshToken).where(RefreshToken.jti == jti)
        )

        return await self._session.scalar(stmt)

    async def get_active_by_jti(self, jti: UUID) -> RefreshToken | None:
        now = datetime.now(UTC)
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.jti == jti,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now
            )
        )

        return await self._session.scalar(stmt)

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = (
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )

        return await self._session.scalar(stmt)

    async def get_by_user(self, user_id: UUID) -> list[RefreshToken]:
        stmt = (
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )

        return list(await self._session.scalars(stmt))

    async def get_active_by_user(self, user_id: UUID) -> list[RefreshToken]:
        now = datetime.now(UTC)
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now
            )
        )

        return list(await self._session.scalars(stmt))

    async def revoke(self, user_id: UUID, refresh_jti: UUID) -> bool:
        now = datetime.now(UTC)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.jti == refresh_jti,
                RefreshToken.revoked_at.is_(None),
            )
            .values(
                revoked_at=now,
                last_used_at=now
            )
            .returning(RefreshToken.id)
        )
        return await self._session.scalar(stmt) is not None

    async def revoke_all_for_user(self, user_id: UUID) -> int:
        now = datetime.now(UTC)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(
                revoked_at=now,
                last_used_at=now
            )
            .returning(RefreshToken.id)
        )

        result = (await self._session.scalars(stmt)).all()
        return len(result)

    async def replace(self, current: RefreshToken, replacement: RefreshToken) -> None:
        current.revoke(replacement)
        self._session.add(replacement)

    async def delete_expired(self) -> int:
        stmt = (
            delete(RefreshToken)
            .where(
                RefreshToken.expires_at < datetime.now(UTC)
            )
            .returning(RefreshToken.id)
        )

        result = (await self._session.scalars(stmt)).all()
        return len(result)
