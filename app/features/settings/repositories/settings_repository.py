from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.exceptions.settings_exceptions import SettingsNotFoundError
from app.features.settings.models.setting import Setting


class SettingsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Setting, not_found_exception=SettingsNotFoundError)

    async def get_all(self) -> list[Setting]:
        stmt = (
            select(Setting)
        )

        return list(await self._session.scalars(stmt))

    async def required_by_key(self, key: SettingsCode) -> Setting:
        stmt = (
            select(Setting)
            .where(Setting.code == key)
        )

        setting = await self._session.scalar(stmt)

        if setting is None:
            raise SettingsNotFoundError(key=key)

        assert setting is not None

        return setting
