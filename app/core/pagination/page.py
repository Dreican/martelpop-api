from math import ceil
from typing import TypeVar, Generic, Callable

from pydantic import BaseModel, computed_field

T = TypeVar("T")
U = TypeVar("U")

class Page(BaseModel, Generic[T]):
    items: list[T]

    page: int
    page_size: int

    total: int


    @computed_field
    @property
    def page_count(self) -> int:
        return ceil(self.total / self.page_size)

    @computed_field
    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page < self.page_count

    def map(self, mapper: Callable[[T], U]) -> Page[U]:

        return Page(
            items=[mapper(item) for item in self.items],
            page=self.page,
            page_size=self.page_size,
            total=self.total,
        )