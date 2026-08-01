from dataclasses import dataclass
from uuid import UUID

from app.features.auth.dependencies.current_principal import unauthorized
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.models.role import Role
from app.features.users.models.user import User


@dataclass(frozen=True, slots=True)
class Principal:
    user: User | None
    role: Role
    permissions: frozenset[PermissionCode]

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None

    @property
    def id(self) -> UUID | None:
        return self.user.id if self.user else None

    @property
    def fullname(self) -> str:
        if self.user is None:
            return "Anonymous"

        return f"{self.user.firstname} {self.user.lastname}"

    @property
    def display_name(self) -> str:
        return self.user.display_name if self.user else "Anonymous"

    @property
    def email(self) -> str :
        return self.user.email if self.user else "Anonymous"

    @property
    def is_admin(self) -> bool:
        return self.role.code == RoleCode.ADMIN

    @property
    def is_vip(self) -> bool:
        return self.role.code == RoleCode.VIP

    @property
    def is_organizer(self) -> bool:
        return self.role.code == RoleCode.ORGANIZER

    def require_authenticated(self) -> AuthenticatedPrincipal:
        if not self.is_authenticated:
            unauthorized("Authentication required.")

        assert self.user is not None

        return AuthenticatedPrincipal(self.user, self.role, self.permissions)


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal(Principal):
    user: User