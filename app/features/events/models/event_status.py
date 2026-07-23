from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.features.events.enums.event_status_code import EventStatusCode

if TYPE_CHECKING:
    from app.features.events.models.event import Event


class EventStatus(Base):
    __tablename__ = "event_statuses"

    code: Mapped[EventStatusCode] = mapped_column(
        Enum(
            EventStatusCode,
            values_callable=lambda e: [i.value for i in e],
            native_enum=False,
        ),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None]

    is_default: Mapped[bool] = mapped_column(default=False)
    sort_order: Mapped[int] = mapped_column(default=0)
    is_public: Mapped[bool] = mapped_column(default=True)
    is_bookable: Mapped[bool] = mapped_column(default=True)
    allow_edit: Mapped[bool] = mapped_column(default=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="status"
    )
