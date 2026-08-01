from typing import Annotated

from fastapi import Depends

from app.features.auth.dependencies.authorization import AuthorizationServiceDep
from app.features.auth.dependencies.current_principal import CurrentPrincipalDep, AuthenticatedPrincipalDep, \
    unauthorized
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal


class RequirePermission:
    def __init__(self, *permissions: PermissionCode):
        self._permissions = frozenset(permissions)

    async def __call__(self, principal: CurrentPrincipalDep, authorization: AuthorizationServiceDep) -> Principal:
        await authorization.require_all_permissions(principal, self._permissions)
        return principal


def require_permission(*permissions: PermissionCode) -> type[AuthenticatedPrincipal]:
    return Annotated[
        AuthenticatedPrincipal,
        Depends(RequirePermission(*permissions)),
    ]


class RequireAuthenticatedPermission:

    def __init__(self, *permissions: PermissionCode):
        self._permissions = frozenset(permissions)

    async def __call__(
        self,
        principal: CurrentPrincipalDep,
        authorization: AuthorizationServiceDep,
    ) -> AuthenticatedPrincipal:

        if principal.user is None:
            unauthorized("Authentication required.")

        await authorization.require_all_permissions(
            principal,
            self._permissions,
        )

        return AuthenticatedPrincipal(
            user=principal.user,
            role=principal.role,
            permissions=principal.permissions,
        )



def require_authenticated_permission(*permissions: PermissionCode):
    return Annotated[
        AuthenticatedPrincipal,
        Depends(RequireAuthenticatedPermission(*permissions))
    ]


def authenticated_permission(*permissions: PermissionCode):
    return Depends(
        RequireAuthenticatedPermission(*permissions)
    )

def permission(*permissions: PermissionCode):
    return Depends(
        RequirePermission(*permissions)
    )