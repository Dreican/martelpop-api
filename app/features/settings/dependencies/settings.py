from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.settings.cache.settings_cache import SettingsCache
from app.features.settings.repositories.settings_repository import SettingsRepository
from app.features.settings.services.application_settings import ApplicationSettings
from app.features.settings.services.settings_service import SettingsService


def get_settings_repository(session: SessionDep) -> SettingsRepository:
    return SettingsRepository(session)


SettingsRepositoryDep = Annotated[SettingsRepository, Depends(get_settings_repository)]

@lru_cache
def get_settings_cache(settings_repository: SettingsRepositoryDep) -> SettingsCache:
    return SettingsCache(settings_repository)


SettingsCacheDep = Annotated[SettingsCache, Depends(get_settings_cache)]


def get_settings_service(
        session: SessionDep,
        settings_repository: SettingsRepositoryDep,
        settings_cache: SettingsCacheDep
) -> SettingsService:
    return SettingsService(session, settings_repository, settings_cache)


SettingsServiceDep = Annotated[SettingsService, Depends(get_settings_service)]


@lru_cache
def get_application_settings(cache: SettingsCacheDep) -> ApplicationSettings:
    return ApplicationSettings(cache)


ApplicationSettingsDep = Annotated[
    ApplicationSettings,
    Depends(get_application_settings),
]