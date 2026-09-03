from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config.configuration import get_config
from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import UserResponseFactoryDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.auth.dependencies.authorization import PermissionCacheDep
from app.features.auth.dependencies.repositories import (
    RoleRepositoryDep,
    AuthenticationIdentityRepositoryDep,
    RefreshTokenRepositoryDep
)
from app.features.auth.security.password_policy import PasswordPolicy
from app.features.auth.services.auth_service import AuthService
from app.features.auth.services.jwt_service import JwtService
from app.features.auth.services.password_service import PasswordService
from app.features.auth.services.principal_service import PrincipalService
from app.features.auth.validators.password_validator import PasswordValidator
from app.features.users.dependencies.repositories import UserRepositoryDep


@lru_cache
def get_password_service() -> PasswordService:
    return PasswordService()


PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]


@lru_cache
def get_jwt_service() -> JwtService:
    config = get_config()
    return JwtService(config.jwt)


JwtServiceDep = Annotated[JwtService, Depends(get_jwt_service)]


def get_principal_service(
        user_repository: UserRepositoryDep,
        role_repository: RoleRepositoryDep,
        jwt_service: JwtServiceDep,
        permission_cache: PermissionCacheDep
) -> PrincipalService:
    return PrincipalService(
        user_repository=user_repository, role_repository=role_repository, jwt_service=jwt_service,
        permission_cache=permission_cache
    )


PrincipalServiceDep = Annotated[PrincipalService, Depends(get_principal_service)]

def get_password_validator() -> PasswordValidator:
    return PasswordValidator(PasswordPolicy())

PasswordValidatorDep = Annotated[PasswordValidator, Depends(get_password_validator)]

def get_auth_service(
        session: SessionDep,
        user: UserRepositoryDep,
        role: RoleRepositoryDep,
        authentication_identity: AuthenticationIdentityRepositoryDep,
        refresh_token: RefreshTokenRepositoryDep,
        password_service: PasswordServiceDep,
        jwt_service: JwtServiceDep,
        slug_service: SlugServiceDep,
        password_validator: PasswordValidatorDep,
        user_response_factory: UserResponseFactoryDep
) -> AuthService:
    return AuthService(
        session=session,
        user_repository=user,
        role_repository=role,
        authentication_identity_repository=authentication_identity,
        password_service=password_service,
        jwt_service=jwt_service,
        refresh_token_repository=refresh_token,
        slug_service=slug_service,
        password_validator=password_validator,
        user_response_factory=user_response_factory
    )


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
