from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.constraints import ROLES_NAME_UNIQUE
from app.features.auth.enums.role_code import RolesCode

if TYPE_CHECKING:
    from app.features.auth.models.role_permission import RolePermission
    from app.features.users.models.user import User


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("name", name=ROLES_NAME_UNIQUE),
    )

    code: Mapped[RolesCode] = mapped_column(
        Enum(
            RolesCode,
            values_callable=lambda e: [item.value for item in e],
            native_enum=False,
            name="role_code",
        ),
        unique=True,
        nullable=False,
    )
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
