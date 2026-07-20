from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.features.auth.enums.permission_code import PermissionCode

if TYPE_CHECKING:
    from app.features.auth.models.role_permission import RolePermission


class Permission(Base):
    __tablename__ = "permissions"

    code: Mapped[PermissionCode] = mapped_column(
        Enum(
            PermissionCode,
            values_callable=lambda e: [i.value for i in e],
            native_enum=False,
        ),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    description: Mapped[str | None]

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    roles = association_proxy(
        "role_permissions",
        "role"
    )

    def __repr__(self) -> str:
        return f"Permissions(id={self.id!r}, name={self.name!r}, description={self.description!r})"
