from app.shared.database.base import Base
from app.shared.database.mixin import IdMixin, TimestampMixin


class Dashboard(Base, IdMixin, TimestampMixin):
    __tablename__ = "dashboard"
    pass
