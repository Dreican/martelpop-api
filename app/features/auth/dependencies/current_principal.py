from typing import Annotated

from fastapi import Depends

from app.features.auth.dependencies.authorization import PermissionCacheDep, AuthorizationRepositoryDep
from app.features.auth.dependencies.current_user import authenticate_user, Credentials
from app.features.auth.dependencies.services import JwtServiceDep
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.security.principal import Principal
from app.features.users.dependencies.repositories import UserRepositoryDep


async def get_current_principal(
        credential: Credentials,
        jwt: JwtServiceDep,
        users: UserRepositoryDep,
        authorization: AuthorizationRepositoryDep,
        cache: PermissionCacheDep
) -> Principal:
    user = await authenticate_user(credential, jwt, users)

    if user is None:
        role = RoleCode.ANONYMOUS
    else:
        role = user.role.code

    permissions = cache.get(role)

    if permissions is None:
        permissions = await authorization.get_permission_codes(role)
        cache.add(role, permissions)

    return Principal(user=user, role=role, permissions=frozenset(permissions))


CurrentPrincipal = Annotated[
    Principal,
    Depends(get_current_principal),
]
