from dataclasses import dataclass


@dataclass(frozen=True)
class PageSettings:
    page_size: int
    max_page_size: int
