from uuid import UUID

from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        UUID: Uuid,
    }
