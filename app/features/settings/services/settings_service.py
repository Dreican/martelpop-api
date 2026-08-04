from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_service import BaseService
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.dto.settings_update_request import SettingsUpdateRequest
from app.features.settings.models.settings import Settings
from app.features.settings.repositories.settings_repository import SettingsRepository


class SettingsService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            settings_repository: SettingsRepository,
            settings_cache: SettingsCache
    ):
        super().__init__(session)
        self._repository = settings_repository
        self._cache = settings_cache


    async def get_settings(self):
        return await self._cache.get_all()


    async def update_settings(self, request: SettingsUpdateRequest, principal: AuthenticatedPrincipal):
        settings = await self._repository.get_by_key(request.key)

        if settings.string_value is not None:
            settings.string_value = request.string_value
        elif settings.int_value is not None:
            settings.int_value = request.int_value
        elif settings.bool_value is not None:
            settings.bool_value = request.bool_value
        else:
            raise ValueError("Invalid settings key")

        return self._persist(settings)



    async def _persist(self, settings: Settings) -> Settings:
        await self._commit()
        await self._refresh(settings)
        self._cache.clear()

        return settings