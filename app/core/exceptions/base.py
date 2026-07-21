from fastapi import status


class ApplicationError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "application_error"
    detail: str = "Application error"

    def __init__(self, detail: str = "Application error") -> None:
        self.detail = detail

        super().__init__(self.detail)
