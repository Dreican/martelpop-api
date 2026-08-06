from app.core.exceptions.not_found import NotFoundError


class SettingsNotFoundError(NotFoundError):
    code = "settings_not_found"
    detail = "Settings not found"
