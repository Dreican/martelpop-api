from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin

if TYPE_CHECKING:
    from app.features.auth.models.role_permission import RolePermission
    from app.features.users.models.user import User


class Role(Base, IdMixin, TimestampMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    description: Mapped[str | None]

    is_default: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="role"
    )

    permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Roles(id={self.id!r}, name={self.name!r}, description={self.description!r})"
