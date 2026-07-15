from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.dependencies.config import JwtConfig
from app.core.dependencies.database import Session
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
from app.features.auth.repositories.refresh_token_repository import RefreshTokenRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.services.authentication_service import AuthenticationService
from app.features.auth.services.jwt_service import JwtService
from app.features.auth.services.password_service import PasswordService
from app.features.users.dependencies import UserRepositoryDep


def get_role_repository(session: Session) -> RoleRepository:
    return RoleRepository(session)


def get_authentication_identity_repository(session: Session) -> AuthenticationIdentityRepository:
    return AuthenticationIdentityRepository(session)


def get_refresh_token_repository(session: Session) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()


@lru_cache
def get_jwt_service(config: JwtConfig) -> JwtService:
    return JwtService(config)


def get_authentication_service(
        session: Session,
        user: UserRepositoryDep,
        role: RoleRepositoryDep,
        authentication_identity: AuthenticationIdentityRepositoryDep,
        refresh_token: RefreshTokenRepositoryDep,
        password_service: PasswordService,
        jwt_service: JwtServiceDep,
        jwt_config: JwtConfig
) -> AuthenticationService:
    return AuthenticationService(
        session=session,
        user_repository=user,
        role_repository=role,
        authentication_identity_repository=authentication_identity,
        password_service=password_service,
        jwt_service=jwt_service,
        jwt_config=jwt_config,
        refresh_token_repository=refresh_token
    )


RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]
AuthenticationIdentityRepositoryDep = Annotated[
    AuthenticationIdentityRepository, Depends(get_authentication_identity_repository)]
RefreshTokenRepositoryDep = Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)]

PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]
JwtServiceDep = Annotated[JwtService, Depends(get_jwt_service)]
AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]
