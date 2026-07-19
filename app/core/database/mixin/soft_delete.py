from datetime import datetime

from sqlalchemy.orm import Mapped


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None]
