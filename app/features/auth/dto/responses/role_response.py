from datetime import datetime

from app.features.auth.dto.responses.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse


class RoleResponse(RoleSummaryResponse):
    description: str
    permissions: list[PermissionSummaryResponse]
    is_default: bool
    created_at: datetime
    updated_at: datetime

