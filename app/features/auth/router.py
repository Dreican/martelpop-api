from fastapi import APIRouter, status
from fastapi.openapi.models import Response

from app.features.auth.dependencies.current_user import CurrentUser
from app.features.auth.dependencies.services import AuthenticationServiceDep
from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.logout_request import LogoutRequest
from app.features.auth.dto.refresh_request import RefreshRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.session_info import SessionInfo
from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.dto.user_response import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, auth: AuthenticationServiceDep, session: SessionInfo) -> TokenResponse:
    return await auth.register(request, session)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, auth: AuthenticationServiceDep, session: SessionInfo) -> TokenResponse:
    return await auth.login(request, session)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(request: RefreshRequest, auth: AuthenticationServiceDep, session: SessionInfo) -> TokenResponse:
    return await auth.refresh(request, session)


@router.post("/logout")
async def logout(request: LogoutRequest, auth: AuthenticationServiceDep) -> Response:
    await auth.logout(request.refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)
