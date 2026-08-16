from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationSettings:
    page_size: int
    max_page_size: int
