from app.core.exceptions.base import ApplicationError
from app.core.exceptions.not_found import NotFoundError


class StorageFileNotFoundError(NotFoundError):
    code = "storage_file_not_found"
    detail = "File not found."


class InvalidFileTypeError(ApplicationError):
    code = "invalid_file_type"
    detail = "Invalid file type."


class FileTooLargeError(ApplicationError):
    code = "file_too_large"
    detail = "File size exceeds the limit."