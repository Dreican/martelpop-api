from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.enums.settings_key import SettingsKey


class ApplicationSettings:

    def __init__(self, cache: SettingsCache):
        self._cache = cache

    async def default_page_size(self) -> int:
        return (await self._cache.get(SettingsKey.DEFAULT_PAGE_SIZE)).int_value

    async def default_location(self) -> str:
        return (await self._cache.get(SettingsKey.DEFAULT_LOCATION)).string_value

    async def registrations_enabled(self) -> bool:
        return (await self._cache.get(SettingsKey.REGISTRATIONS_ENABLED)).bool_value