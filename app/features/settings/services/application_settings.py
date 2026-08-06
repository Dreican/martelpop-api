from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.enums.settings_key import SettingsKey
from app.features.storage.dto.email_settings import EmailSettings
from app.features.storage.dto.event_settings import EventSettings
from app.features.storage.dto.general_settings import GeneralSettings
from app.features.storage.dto.page_settings import PageSettings
from app.features.storage.dto.registration_settings import RegistrationSettings


class ApplicationSettings:

    def __init__(self, cache: SettingsCache):
        self._cache = cache

    async def general(self) -> GeneralSettings:
        general = GeneralSettings(
            application_name=await self._string(SettingsKey.APPLICATION_NAME),
            logo_url=await self._string(SettingsKey.APPLICATION_LOGO),
            maintenance_mode=await self._bool(SettingsKey.MAINTENANCE_MODE)
        )
        return general

    async def page_settings(self) -> PageSettings:
        pages = PageSettings(
            page_size=await self._int(SettingsKey.DEFAULT_PAGE_SIZE),
            max_page_size=await self._int(SettingsKey.MAX_PAGE_SIZE)
        )
        return pages


    async def event_settings(self) -> EventSettings:
        event_settings = EventSettings(
            event_location=await self._string(SettingsKey.DEFAULT_EVENT_LOCATION),
            event_capacity=await self._int(SettingsKey.DEFAULT_EVENT_CAPACITY),
            duration=await self._int(SettingsKey.DEFAULT_EVENT_DURATION)
        )
        return event_settings

    async def registration_settings(self) -> RegistrationSettings:
        registration_settings = RegistrationSettings(
            registrations_enabled=await self._bool(SettingsKey.REGISTRATIONS_ENABLED),
            waitlist_enabled=await self._bool(SettingsKey.WAITLIST_ENABLED),
            open_days_before=await self._int(SettingsKey.OPEN_DAYS_BEFORE),
            close_hours_before=await self._int(SettingsKey.CLOSE_HOURS_BEFORE)
        )
        return registration_settings

    async def email_settings(self):
        email_settings = EmailSettings(
            enabled=await self._bool(SettingsKey.EMAIL_ENABLE),
            support_email=await self._string(SettingsKey.EMAIL_SUPPORT_ADDRESS),
            reply_to_email=await self._string(SettingsKey.EMAIL_REPLY_TO),
            send_registration_confirmation=await self._bool(SettingsKey.EMAIL_SEND_REGISTRATION_CONFIRMATION),
            send_cancellation_confirmation=await self._bool(SettingsKey.EMAIL_SEND_CANCELLATION_CONFIRMATION),
            send_event_reminders=await self._bool(SettingsKey.EMAIL_SEND_EVENT_REMINDERS),
            reminder_days_before=await self._int(SettingsKey.EMAIL_REMINDER_DAYS_BEFORE)
        )
        return email_settings


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