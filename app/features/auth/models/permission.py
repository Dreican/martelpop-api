from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.mixin.id import IdMixin
from app.core.database.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.features.auth.models.role_permission import RolePermission


class Permission(Base, IdMixin, TimestampMixin):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    description: Mapped[str | None]

    roles: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Permissions(id={self.id!r}, name={self.name!r}, description={self.description!r})"
