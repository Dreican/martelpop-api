from datetime import datetime, UTC

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    detail: str
    timestamp: datetime = datetime.now(UTC)