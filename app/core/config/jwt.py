from datetime import timedelta

from pydantic import SecretStr, BaseModel, computed_field


class JWTConfig(BaseModel):
    secret_key: SecretStr
    algorithm: str = "HS256"
    issuer: str = "martelpop-api"
    audience: str = "martelpop-web"
    access_token_expiration_minutes: int = 15
    refresh_token_expiration_days: int = 30

    @computed_field
    @property
    def access_token_lifetime(self) -> timedelta:
        return timedelta(minutes=self.access_token_expiration_minutes)

    @computed_field
    @property
    def refresh_token_lifetime(self) -> timedelta:
        return timedelta(days=self.refresh_token_expiration_days)
