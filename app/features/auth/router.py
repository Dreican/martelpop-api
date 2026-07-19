from fastapi import APIRouter, status
from fastapi import Response

from app.features.auth.dependencies.current_user import CurrentUser
from app.features.auth.dependencies.services import AuthenticationServiceDep
from app.features.auth.dependencies.session import SessionInfoDep
from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.logout_request import LogoutRequest
from app.features.auth.dto.refresh_request import RefreshRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.token_response import TokenResponse
from app.features.users.dto.user_response import UserResponse
from app.features.users.mappers.user_mapper import UserMapper

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, auth: AuthenticationServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.register(request, session)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="Authenticates a user and returns an access token and refresh token.",
    responses={
        401: {"description": "Invalid credentials"},
        409: {"description": "Email already exists"},
    }
)
async def login(request: LoginRequest, auth: AuthenticationServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.login(request, session)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh(request: RefreshRequest, auth: AuthenticationServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.refresh(request.refresh_token, session)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: LogoutRequest, auth: AuthenticationServiceDep) -> Response:
    await auth.logout(request.refresh_token)
    return Response()


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(current_user: CurrentUser, auth: AuthenticationServiceDep) -> Response:
    await auth.logout_all(current_user.id)
    return Response()


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser) -> UserResponse:
    return UserMapper.to_response(current_user)
