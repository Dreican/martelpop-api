from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.models.permission import Permission


class PermissionSummaryResponseFactory(ResponseFactory[Permission, PermissionSummaryResponse]):
    def __init__(self):
        super().__init__()

    def create(self, entity: Permission) -> PermissionSummaryResponse:
        response = PermissionSummaryResponse.model_validate(entity)

        return response
