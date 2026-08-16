from app.features.auth.dto.responses.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse


class PermissionResponse(PermissionSummaryResponse):
    description: str
    roles: list[RoleSummaryResponse]
