from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.enums.settings_key import SettingsKey
from app.features.storage.dto.general_settings import GeneralSettings


class ApplicationSettings:

    def __init__(self, cache: SettingsCache):
        self._cache = cache

    async def general(self) -> GeneralSettings:
        general = GeneralSettings(
            application_name=await self._string(SettingsKey.APPLICATION_NAME),
            logo_url=await self._string(SettingsKey.APPLICATION_LOGO),
            support_email=await self._string(SettingsKey.APPLICATION_SUPPORT_EMAIL),
            maintenance_mode=await self._bool(SettingsKey.MAINTENANCE_MODE)
        )
        return general

    async def default_page_size(self) -> int:
        return await self._int(SettingsKey.DEFAULT_PAGE_SIZE)

    async def max_page_size(self) -> int:
        return await self._int(SettingsKey.MAX_PAGE_SIZE)

    async def default_event_location(self) -> str:
        return await self._string(SettingsKey.DEFAULT_EVENT_LOCATION)

    async def default_event_capacity(self) -> int:
        return await self._int(SettingsKey.DEFAULT_EVENT_CAPACITY)

    async def registrations_enabled(self) -> bool:
        return await self._bool(SettingsKey.REGISTRATIONS_ENABLED)


    async def _int(self, key: SettingsKey) -> int:
        setting = await self._cache.get(key)
        assert setting.int_value is not None
        return setting.int_value

    async def _bool(self, key: SettingsKey) -> bool:
        setting = await self._cache.get(key)
        assert setting.bool_value is not None
        return setting.bool_value

    async def _string(self, key: SettingsKey) -> str:
        setting = await self._cache.get(key)
        assert setting.string_value is not None
        return setting.string_value