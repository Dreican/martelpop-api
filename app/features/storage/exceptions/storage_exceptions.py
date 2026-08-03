from app.core.exceptions.not_found import NotFoundError


class StorageFileNotFoundError(NotFoundError):
    code = "storage_file_not_found"
    detail = "File not found."