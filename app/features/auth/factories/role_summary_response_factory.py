from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.auth.models.role import Role
from app.features.storage.services.sotrage_service import StorageService


class RoleSummaryResponseFactory(ResponseFactory[Role, RoleSummaryResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: Role) -> RoleSummaryResponse:
        response = RoleSummaryResponse.model_validate(entity)

        return response
