from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class SlugMixin:
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
