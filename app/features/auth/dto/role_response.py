from app.features.auth.dto.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.dto.role_summary_response import RoleSummaryResponse


class RoleResponse(RoleSummaryResponse):
    description: str
    permission: list[PermissionSummaryResponse]
