from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )
