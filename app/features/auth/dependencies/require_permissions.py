from fastapi import Depends

from app.features.auth.dependencies.authorization import AuthorizationServiceDep
from app.features.auth.dependencies.current_principal import CurrentPrincipalDep
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.helper import unauthorized
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal


class PermissionDependency:
    def __init__(self, *permissions: PermissionCode):
        self._permissions = frozenset(permissions)

    async def __call__(self, principal: CurrentPrincipalDep, authorization: AuthorizationServiceDep) -> Principal:
        authorization.require_all_permissions(principal, self._permissions)
        return principal


class AuthenticatedPermissionDependency(PermissionDependency):

    async def __call__(
            self,
            principal: CurrentPrincipalDep,
            authorization: AuthorizationServiceDep,
    ) -> AuthenticatedPrincipal:
        principal = await super().__call__(principal, authorization)

        if principal.user is None:
            unauthorized("Authentication required.")

        return principal.require_authenticated()


def permission(*permissions: PermissionCode):
    return Depends(
        PermissionDependency(*permissions)
    )


def authenticated_permission(*permissions: PermissionCode):
    return Depends(
        AuthenticatedPermissionDependency(*permissions)
    )
