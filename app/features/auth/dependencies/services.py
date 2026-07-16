from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.dependencies.config import JwtConfig, SettingsDep
from app.core.dependencies.database import Session
from app.features.auth.dependencies.repositories import RoleRepositoryDep, AuthenticationIdentityRepositoryDep, \
    RefreshTokenRepositoryDep

from app.features.auth.services.authentication_service import AuthenticationService
from app.features.auth.services.jwt_service import JwtService
from app.features.auth.services.password_service import PasswordService
from app.features.users.dependencies import UserRepositoryDep


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()


@lru_cache
def get_jwt_service(settings: SettingsDep) -> JwtService:
    return JwtService(settings.jwt)


def get_authentication_service(
        session: Session,
        user: UserRepositoryDep,
        role: RoleRepositoryDep,
        authentication_identity: AuthenticationIdentityRepositoryDep,
        refresh_token: RefreshTokenRepositoryDep,
        password_service: PasswordServiceDep,
        jwt_service: JwtServiceDep,
) -> AuthenticationService:
    return AuthenticationService(
        session=session,
        user_repository=user,
        role_repository=role,
        authentication_identity_repository=authentication_identity,
        password_service=password_service,
        jwt_service=jwt_service,
        refresh_token_repository=refresh_token
    )


PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]
JwtServiceDep = Annotated[JwtService, Depends(get_jwt_service)]
AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]