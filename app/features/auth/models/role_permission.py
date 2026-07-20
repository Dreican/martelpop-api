from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import ROLE_PERMISSION_UNIQUE

if TYPE_CHECKING:
    from app.features.auth.models.permission import Permission
    from app.features.auth.models.role import Role


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name=ROLE_PERMISSION_UNIQUE,
        ),
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True
    )

    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permissions.id"),
        primary_key=True
    )

    role: Mapped["Role"] = relationship(
        back_populates="role_permissions"
    )

    permission: Mapped["Permission"] = relationship(
        back_populates="role_permissions"
    )
