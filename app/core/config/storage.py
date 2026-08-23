from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class StorageConfig(BaseModel):
    type: Literal["local"] = "local"
    base_path: Path = Path("/app/storage")
    public_base_url: str = "/files"
    max_upload_size: int = 10485760
    allowed_content_types: list[str] = ["image/jpeg", "image/png", "image/webp"]
