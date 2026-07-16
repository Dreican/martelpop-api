from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import Session
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
from app.features.auth.repositories.refresh_token_repository import RefreshTokenRepository
from app.features.auth.repositories.role_repository import RoleRepository


def get_role_repository(session: Session) -> RoleRepository:
    return RoleRepository(session)


def get_authentication_identity_repository(session: Session) -> AuthenticationIdentityRepository:
    return AuthenticationIdentityRepository(session)


def get_refresh_token_repository(session: Session) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)

RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]
AuthenticationIdentityRepositoryDep = Annotated[AuthenticationIdentityRepository, Depends(get_authentication_identity_repository)]
RefreshTokenRepositoryDep = Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)]