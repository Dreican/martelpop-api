from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_service import BaseService
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.dto.settings_update_request import SettingsUpdateRequest
from app.features.settings.enums.settings_type import SettingsType
from app.features.settings.models.settings import Settings
from app.features.settings.repositories.settings_repository import SettingsRepository
from app.features.settings.services.application_settings import ApplicationSettings


class SettingsService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            settings_repository: SettingsRepository,
            settings_cache: SettingsCache,
            application_settings: ApplicationSettings
    ):
        super().__init__(session)
        self._repository = settings_repository
        self._cache = settings_cache
        self._application_settings = application_settings

    async def get_settings(self):
        return await self._cache.get_all()

    async def update_settings(self, request: SettingsUpdateRequest, principal: AuthenticatedPrincipal):
        settings = await self._repository.required_by_key(request.key)

        match settings.value_type:
            case SettingsType.STRING:
                settings.string_value = cast(str, request.value)
            case SettingsType.INTEGER:
                settings.int_value = cast(int, request.value)
            case SettingsType.BOOLEAN:
                settings.bool_value = cast(bool, request.value)

        return self._persist(settings)

    async def _persist(self, settings: Settings) -> Settings:
        await self._commit()
        await self._refresh(settings)
        await self._cache.reload()
        await self._application_settings.reload()

        return settings
