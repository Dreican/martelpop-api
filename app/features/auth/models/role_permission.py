from uuid import UUID
from sqlalchemy import UniqueConstraint, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin


class RolePermission(Base, IdMixin, TimestampMixin):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission",
        ),
    )

    role_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("roles.id")
    )

    permission_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("permissions.id")
    )

    role: Mapped["Role"] = relationship(
        back_populates="permissions"
    )

    permission: Mapped["Permission"] = relationship(
        back_populates="roles"
    )
