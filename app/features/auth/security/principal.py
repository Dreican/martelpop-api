from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy.ext.hybrid import hybrid_property

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode
from app.features.users.models.user import User


@dataclass(slots=True)
class Principal:
    user: User | None
    role: RoleCode
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
        return self.role == RoleCode.ADMIN

    @property
    def is_vip(self) -> bool:
        return self.role == RoleCode.VIP

    @property
    def is_organizer(self) -> bool:
        return self.role == RoleCode.ORGANIZER