from app.core.factories.response_factory import ResponseFactory
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.models.stored_file import StoredFile


class StoredFileResponseFactory(ResponseFactory[StoredFile, StoredFileResponse]):
    def __init__(self):
        super().__init__()

    def create(self, entity: StoredFile) -> StoredFileResponse:
        response: StoredFileResponse = super().create(entity)
        response.url = self.file_url(entity.id)

        return response
