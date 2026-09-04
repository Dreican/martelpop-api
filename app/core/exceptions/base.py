import logging
from typing import Any

from fastapi import status

logger = logging.getLogger("ApplicationError")

class ApplicationError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "application_error"
    detail: str = "Application error"

    def __init__(self, detail: str | None = None, **context: Any) -> None:
        if detail is not None:
            self.detail = detail

        self.context: dict[str, Any] = context

        super().__init__(self.detail)

        logger.error(self.detail, context)
