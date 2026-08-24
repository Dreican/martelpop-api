from typing import Literal

from pydantic import BaseModel


class CookieConfig(BaseModel):
    secure: bool = True
    samesite: Literal["lax", "strict", "none"] = "lax"
