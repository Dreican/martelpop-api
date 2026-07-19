from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        UUID: Uuid,
        datetime: TIMESTAMP(timezone=True),
    }
