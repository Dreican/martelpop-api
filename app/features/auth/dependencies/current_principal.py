from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.features.auth.dependencies.authorization import PermissionCacheDep
from app.features.auth.dependencies.repositories import RoleRepositoryDep
from app.features.auth.dependencies.services import JwtServiceDep
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.helper import unauthorized
from app.features.auth.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from app.features.auth.security.bearer import bearer_scheme
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.users.dependencies.repositories import UserRepositoryDep
from app.features.users.models.user import User

Credentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme)
]


async def authenticate_user(
        credentials: Credentials,
        jwt: JwtServiceDep,
        users: UserRepositoryDep
) -> User | None:

    if credentials is None:
        return None

    try:
        payload = jwt.decode_access_token(str(credentials.credentials))
    except (ExpiredTokenError, InvalidTokenError):
        return None

    user = await users.get_by_id(payload.sub)

    if (
        user is None
        or not user.is_active
        or user.is_deleted
    ):
        return None

    return user

async def get_current_principal(
        credential: Credentials,
        jwt: JwtServiceDep,
        users: UserRepositoryDep,
        roles: RoleRepositoryDep,
        cache: PermissionCacheDep
) -> Principal:
    user = await authenticate_user(credential, jwt, users)

    if user is None:
        role = await roles.require_by_code(RoleCode.ANONYMOUS)
    else:
        role = user.role

    permissions = await cache.get_permissions(role.code)

    return Principal(user=user, role=role, permissions=frozenset(permissions))


CurrentPrincipalDep = Annotated[
    Principal,
    Depends(get_current_principal),
]


async def get_authenticated_principal(principal: CurrentPrincipalDep) -> AuthenticatedPrincipal:

    if principal.user is None:
        unauthorized("Not authenticated")

    assert principal.user is not None

    return AuthenticatedPrincipal(
        user=principal.user,
        role=principal.role,
        permissions=frozenset(principal.permissions),
    )


AuthenticatedPrincipalDep = Annotated[
    AuthenticatedPrincipal,
    Depends(get_authenticated_principal),
]