from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.auth.models.role import Role


class RoleSummaryResponseFactory(ResponseFactory[Role, RoleSummaryResponse]):
    def __init__(self):
        super().__init__()

    def create(self, entity: Role) -> RoleSummaryResponse:
        response = RoleSummaryResponse.model_validate(entity)

        return response
