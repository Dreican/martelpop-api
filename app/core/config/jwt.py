from pydantic import SecretStr, BaseModel


class JWTConfig(BaseModel):
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expiration_minutes: int = 15
    refresh_token_expiration_days: int = 30
