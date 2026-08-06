from uuid import UUID

from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.dto.branding_settings import BrandingSettings
from app.features.settings.dto.email_settings import EmailSettings
from app.features.settings.dto.event_settings import EventSettings
from app.features.settings.dto.general_settings import GeneralSettings
from app.features.settings.dto.page_settings import PaginationSettings
from app.features.settings.dto.registration_settings import RegistrationSettings
from app.features.settings.enums.settings_key import SettingsCode


class ApplicationSettings:

    def __init__(self, cache: SettingsCache):
        self._cache = cache

    async def general(self) -> GeneralSettings:
        return GeneralSettings(
            maintenance_mode=await self._bool(SettingsCode.MAINTENANCE_MODE),
            application_url=await self._string(SettingsCode.APPLICATION_URL),
            support_email=await self._string(SettingsCode.SUPPORT_EMAIL),
            contact_email=await self._string(SettingsCode.CONTACT_EMAIL),
            reply_to_email=await self._string(SettingsCode.REPLY_TO_EMAIL)
        )

    async def branding(self) -> BrandingSettings:
        return BrandingSettings(
            application_name=await self._string(SettingsCode.APPLICATION_NAME),
            logo_file_id=await self._uuid(SettingsCode.APPLICATION_LOGO),
            favicon_file_id=await self._uuid(SettingsCode.APPLICATION_FAVICON),
            footer_text=await self._string(SettingsCode.FOOTER_TEXT)
        )

    async def pagination(self) -> PaginationSettings:
        return PaginationSettings(
            page_size=await self._int(SettingsCode.DEFAULT_PAGE_SIZE),
            max_page_size=await self._int(SettingsCode.MAX_PAGE_SIZE)
        )

    async def events(self) -> EventSettings:
        return EventSettings(
            event_location=await self._string(SettingsCode.DEFAULT_EVENT_LOCATION),
            event_capacity=await self._int(SettingsCode.DEFAULT_EVENT_CAPACITY),
            duration=await self._int(SettingsCode.DEFAULT_EVENT_DURATION)
        )

    async def registrations(self) -> RegistrationSettings:
        return RegistrationSettings(
            registrations_enabled=await self._bool(SettingsCode.REGISTRATIONS_ENABLED),
            waitlist_enabled=await self._bool(SettingsCode.WAITLIST_ENABLED),
            open_days_before=await self._int(SettingsCode.OPEN_DAYS_BEFORE),
            close_hours_before=await self._int(SettingsCode.CLOSE_HOURS_BEFORE)
        )

    async def emails(self) -> EmailSettings:
        return EmailSettings(
            enabled=await self._bool(SettingsCode.EMAIL_ENABLE),
            send_registration_confirmation=await self._bool(SettingsCode.EMAIL_SEND_REGISTRATION_CONFIRMATION),
            send_cancellation_confirmation=await self._bool(SettingsCode.EMAIL_SEND_CANCELLATION_CONFIRMATION),
            send_event_reminders=await self._bool(SettingsCode.EMAIL_SEND_EVENT_REMINDERS),
            reminder_days_before=await self._int(SettingsCode.EMAIL_REMINDER_DAYS_BEFORE)
        )

    async def _int(self, key: SettingsCode) -> int:
        setting = await self._cache.get(key)
        if setting.int_value is None:
            raise RuntimeError(
                f"Setting '{key.value}' is not configured as an integer."
            )

        return setting.int_value

    async def _bool(self, key: SettingsCode) -> bool:
        setting = await self._cache.get(key)
        if setting.bool_value is None:
            raise RuntimeError(
                f"Setting '{key.value}' is not configured as a boolean."
            )

        return setting.bool_value

    async def _string(self, key: SettingsCode) -> str | None:
        setting = await self._cache.get(key)

        return setting.string_value

    async def _uuid(self, key: SettingsCode) -> UUID | None:
        value = await self._string(key)

        if not value:
            return None

        return UUID(value)
