from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.exceptions.settings_exceptions import SettingsNotFoundError
from app.features.settings.models.settings import Settings


class SettingsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Settings, not_found_exception=SettingsNotFoundError)

    async def get_all(self) -> list[Settings]:
        stmt = (
            select(Settings)
        )

        return list(await self._session.scalars(stmt))

    async def required_by_key(self, key: SettingsCode) -> Settings:
        stmt = (
            select(Settings)
            .where(Settings.code == key)
        )

        setting = await self._session.scalar(stmt)

        if setting is None:
            raise SettingsNotFoundError(key=key)

        assert setting is not None

        return setting
