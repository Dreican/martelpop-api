from pydantic import BaseModel


class PaginationConfig(BaseModel):
    default_page_size_page: int = 20
    max_page_size: int = 100
