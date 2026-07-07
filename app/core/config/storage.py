from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class StorageSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="STORAGE_",
    )

    upload_dir: str = "uploads"
    max_upload_size: int = 10485760
    allowed_image_types: list[str] = ["image/jpeg", "image/png"]
