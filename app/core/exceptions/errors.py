from datetime import datetime, UTC

from pydantic import BaseModel, Field


class FieldError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    code: str
    detail: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    errors: list[FieldError] | None = None
