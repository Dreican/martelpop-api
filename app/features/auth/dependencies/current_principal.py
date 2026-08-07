from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.features.auth.dependencies.authorization import PermissionCacheDep
from app.features.auth.dependencies.repositories import RoleRepositoryDep
from app.features.auth.dependencies.services import JwtServiceDep, AuthenticationServiceDep
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.helper import unauthorized
from app.features.auth.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from app.features.auth.security.bearer import bearer_scheme
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.users.dependencies.repositories import UserRepositoryDep
from app.features.users.models.user import User

CredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme)
]


async def get_current_principal(
        credentials: CredentialsDep,
        authentication: AuthenticationServiceDep,
) -> Principal:
    token = (
        credentials.credentials
        if credentials is not None
        else None
    )

    return await authentication.authenticate(token)


CurrentPrincipalDep = Annotated[
    Principal,
    Depends(get_current_principal),
]


async def get_authenticated_principal(
        principal: CurrentPrincipalDep,
        authentication: AuthenticationServiceDep
) -> AuthenticatedPrincipal:
    return authentication.require_authenticated(principal)


AuthenticatedPrincipalDep = Annotated[
    AuthenticatedPrincipal,
    Depends(get_authenticated_principal),
]
