from uuid import UUID

from app.core.config.pagination import PaginationConfig
from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.dto.branding_settings import BrandingSettings
from app.features.settings.dto.email_settings import EmailSettings
from app.features.settings.dto.event_settings import EventSettings
from app.features.settings.dto.general_settings import GeneralSettings
from app.features.settings.dto.page_settings import PaginationSettings
from app.features.settings.dto.registration_settings import RegistrationSettings
from app.features.settings.enums.settings_key import SettingsKey


class ApplicationSettings:
    _general: GeneralSettings | None = None
    _branding: BrandingSettings | None = None
    _pagination: PaginationSettings | None = None
    _event: EventSettings | None = None
    _registration: RegistrationSettings | None = None
    _email: EmailSettings | None = None

    def __init__(self, cache: SettingsCache):
        self._cache = cache

    async def general(self) -> GeneralSettings:
        if self._general is None:
            self._general = GeneralSettings(
                maintenance_mode=await self._bool(SettingsKey.MAINTENANCE_MODE),
                application_url=await self._string(SettingsKey.APPLICATION_URL),
                support_email=await self._string(SettingsKey.SUPPORT_EMAIL),
                contact_email=await self._string(SettingsKey.CONTACT_EMAIL),
                reply_to_email=await self._string(SettingsKey.REPLY_TO_EMAIL)
            )
        assert self._general is not None
        return self._general

    async def branding(self) -> BrandingSettings:
        if self._branding is None:
            self._branding = BrandingSettings(
                application_name=await self._string(SettingsKey.APPLICATION_NAME),
                logo_file_id=await self._uuid(SettingsKey.APPLICATION_LOGO),
                favicon_file_id=await self._uuid(SettingsKey.APPLICATION_FAVICON),
                footer_text=await self._string(SettingsKey.FOOTER_TEXT)
            )

        assert self._branding is not None
        return self._branding

    async def pagination(self) -> PaginationSettings:
        return PaginationSettings(
            page_size=await self._int(SettingsKey.DEFAULT_PAGE_SIZE),
            max_page_size=await self._int(SettingsKey.MAX_PAGE_SIZE)
        )

    async def event(self) -> EventSettings:
        return EventSettings(
            event_location=await self._string(SettingsKey.DEFAULT_EVENT_LOCATION),
            event_capacity=await self._int(SettingsKey.DEFAULT_EVENT_CAPACITY),
            duration=await self._int(SettingsKey.DEFAULT_EVENT_DURATION)
        )

    async def registration(self) -> RegistrationSettings:
        return RegistrationSettings(
            registrations_enabled=await self._bool(SettingsKey.REGISTRATIONS_ENABLED),
            waitlist_enabled=await self._bool(SettingsKey.WAITLIST_ENABLED),
            open_days_before=await self._int(SettingsKey.OPEN_DAYS_BEFORE),
            close_hours_before=await self._int(SettingsKey.CLOSE_HOURS_BEFORE)
        )

    async def email(self) -> EmailSettings:
        return EmailSettings(
            enabled=await self._bool(SettingsKey.EMAIL_ENABLE),
            support_email=await self._string(SettingsKey.EMAIL_SUPPORT_ADDRESS),
            send_registration_confirmation=await self._bool(SettingsKey.EMAIL_SEND_REGISTRATION_CONFIRMATION),
            send_cancellation_confirmation=await self._bool(SettingsKey.EMAIL_SEND_CANCELLATION_CONFIRMATION),
            send_event_reminders=await self._bool(SettingsKey.EMAIL_SEND_EVENT_REMINDERS),
            reminder_days_before=await self._int(SettingsKey.EMAIL_REMINDER_DAYS_BEFORE)
        )

    async def _int(self, key: SettingsKey) -> int:
        setting = await self._cache.get(key)
        if setting.int_value is None:
            return 0

        return setting.int_value

    async def _bool(self, key: SettingsKey) -> bool:
        setting = await self._cache.get(key)
        if setting.bool_value is None:
            return False

        return setting.bool_value

    async def _string(self, key: SettingsKey) -> str | None:
        setting = await self._cache.get(key)

        return setting.string_value

    async def _uuid(self, key: SettingsKey) -> UUID | None:
        value = await self._string(key)

        if not value:
            return None

        return UUID(value)