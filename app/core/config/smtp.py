from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class SMTPSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="SMTP_",
    )

    host: str
    port: int = 587
    username: str
    password: str
    from_email: str = "noreply@martelpop.dev"
    use_tls: bool = True
