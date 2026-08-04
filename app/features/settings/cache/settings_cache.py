import logging

from app.features.settings.models.settings import Settings
from app.features.settings.repositories.settings_repository import SettingsRepository

logger = logging.getLogger(__name__)

class SettingsCache:
    def __init__(self, settings_repository: SettingsRepository):
        self._repository = settings_repository
        self._cache: dict[str, Settings] | None = None

    def clear(self) -> None:
        if self._cache is not None:
            self._cache.clear()

    async def get(self, key: str) ->  Settings:
        await self._load()
        assert self._cache is not None
        return self._cache[key]

    async def get_all(self) -> list[Settings]:
        await self._load()

        return list(self._settings.values())


    async def _load(self) -> None:
        if self._cache is None:
            settings = await self._repository.get_all()

            self._settings = {
                s.key: s
                for s in settings
            }