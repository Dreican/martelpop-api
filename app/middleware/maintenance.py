from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.features.auth.services.authentication_service import AuthenticationService
from app.features.settings.services.application_settings import ApplicationSettings


class MaintenanceMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = {
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc"
    }

    def __init__(
            self,
            app,
            authentication: AuthenticationService,
            settings: ApplicationSettings,
    ):
        super().__init__(app)
        self._authentication = authentication
        self._settings = settings

    async def dispatch(self, request, call_next):

        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        general = await self._settings.general()

        if not general.maintenance_mode:
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        token = self._authentication.extract_token(authorization)

        principal = await self._authentication.authenticate(token)

        if principal.is_admin:
            return await call_next(request)

        return JSONResponse(content={"detail": "The application is currently under maintenance."}, status_code=503)