from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.models.permission import Permission
from app.features.storage.services.sotrage_service import StorageService


class PermissionSummaryResponseFactory(ResponseFactory[Permission, PermissionSummaryResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: Permission) -> PermissionSummaryResponse:
        response = PermissionSummaryResponse.model_validate(entity)

        return response
