import logging

from app.features.settings.models.settings import Settings
from app.features.settings.repositories.settings_repository import SettingsRepository

logger = logging.getLogger(__name__)

class SettingsCache:
    def __init__(self, settings_repository: SettingsRepository):
        self._repository = settings_repository
        self._cache: dict[str, Settings] | None = None
        self._loaded = False

    def get(self, key: str) -> Settings | None:
        return self._cache.get(key)

    def add(self, key: str, value: Settings) -> None:
        self._cache[key] = value

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        if self._cache is not None:
            self._cache.clear()
            self._loaded = False

    async def _load(self) -> None:
        if self._cache is None:
            settings = await self._repository.get_all()

            self._settings = {
                s.key: s
                for s in settings
            }

    async def get_setting(self, key: str) ->  Settings:
        await self._load()

        return self._cache[key]

    async def get_all(self) -> list[Settings]:
        await self._load()

        return list(self._settings.values())
