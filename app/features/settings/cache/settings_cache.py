import logging

from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.models.settings import Settings
from app.features.settings.repositories.settings_repository import SettingsRepository

logger = logging.getLogger(__name__)


class SettingsCache:
    def __init__(self, settings_repository: SettingsRepository):
        self._repository = settings_repository
        self._cache: dict[SettingsCode, Settings] | None = None

    async def reload(self) -> None:
        self._cache = None
        await self._load()

    async def get(self, code: SettingsCode) -> Settings:
        await self._load()
        assert self._cache is not None
        return self._cache[code]

    async def get_all(self) -> list[Settings]:
        await self._load()
        assert self._cache is not None
        return list(self._cache.values())

    async def _load(self) -> None:
        if self._cache is None:
            settings = await self._repository.get_all()

            self._cache = {
                setting.code: setting
                for setting in settings
            }
