from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.auth.cache.permission_cache import PermissionCache
from app.features.auth.repositories.authorization_repository import AuthorizationRepository
from app.features.auth.services.authorization_service import AuthorizationService


@lru_cache
def get_permission_cache() -> PermissionCache:
    return PermissionCache()


PermissionCacheDep = Annotated[PermissionCache, Depends(get_permission_cache)]


def get_authorization_repository(session: SessionDep) -> AuthorizationRepository:
    return AuthorizationRepository(session)


AuthorizationRepositoryDep = Annotated[AuthorizationRepository, Depends(get_authorization_repository)]


def get_authorization_service(repository: AuthorizationRepositoryDep,
                              cache: PermissionCacheDep, ) -> AuthorizationService:
    return AuthorizationService(authorization_repository=repository, permission_cache=cache)


AuthorizationServiceDep = Annotated[AuthorizationService, Depends(get_authorization_service)]
