from typing import Annotated

from fastapi import Request, Depends

from app.features.auth.dto.session_info import SessionInfo


def get_session_info(request: Request) -> SessionInfo:
    return SessionInfo(
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
        device_name=None,
    )


SessionInfoDep = Annotated[SessionInfo, Depends(get_session_info)]
