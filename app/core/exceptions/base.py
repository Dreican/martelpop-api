from starlette.status import HTTP_400_BAD_REQUEST


class ApplicationError(Exception):
    status_code: int = HTTP_400_BAD_REQUEST
    code: str = "application_error"
    detail: str = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail

        super().__init__(self.detail)
