from typing import Annotated

from fastapi import Depends

from app.features.auth.dependencies.authorization import PermissionCacheDep, AuthorizationRepositoryDep
from app.features.auth.dependencies.current_user import authenticate_user, Credentials, unauthorized
from app.features.auth.dependencies.repositories import RoleRepositoryDep
from app.features.auth.dependencies.services import JwtServiceDep
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.users.dependencies.repositories import UserRepositoryDep


async def get_current_principal(
        credential: Credentials,
        jwt: JwtServiceDep,
        users: UserRepositoryDep,
        roles: RoleRepositoryDep,
        authorization: AuthorizationRepositoryDep,
        cache: PermissionCacheDep
) -> Principal:
    user = await authenticate_user(credential, jwt, users)

    if user is None:
        role = await roles.require_by_code(RoleCode.ANONYMOUS)
    else:
        role = user.role

    permissions = cache.get(role.code)

    if permissions is None:
        permissions = await authorization.get_permission_codes(role.code)
        cache.add(role.code, permissions)

    return Principal(user=user, role=role, permissions=frozenset(permissions))


CurrentPrincipal = Annotated[
    Principal,
    Depends(get_current_principal),
]


async def get_authenticated_principal(principal: CurrentPrincipal) -> AuthenticatedPrincipal:

    if principal.user is None:
        unauthorized("Not authenticated")

    assert principal.user is not None

    return AuthenticatedPrincipal(
        user=principal.user,
        role=principal.role,
        permissions=principal.permissions,
    )


AuthenticatedPrincipal = Annotated[
    AuthenticatedPrincipal,
    Depends(get_authenticated_principal),
]