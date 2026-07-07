from pydantic import BaseModel


class StorageConfig(BaseModel):
    upload_dir: str = "uploads"
    max_upload_size: int = 10485760
    allowed_image_types: list[str] = ["image/jpeg", "image/png"]
