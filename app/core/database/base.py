from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase

from app.core.database.mixin.id import IdMixin
from app.core.database.mixin.timestamp import TimestampMixin


class Base(IdMixin, TimestampMixin, DeclarativeBase):
    type_annotation_map = {
        UUID: Uuid,
        datetime: TIMESTAMP(timezone=True),
    }


