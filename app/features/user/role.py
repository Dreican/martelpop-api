from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base

if TYPE_CHECKING:
    from app.features.user.models import User

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    description: Mapped[str | None]

    users: Mapped[list["User"]] = relationship(
        back_populates="role"
    )

    def __repr__(self) -> str:
        return f"Roles(id={self.id!r}, name={self.name!r}, description={self.description!r})"