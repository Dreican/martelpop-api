from typing import TypeVar, Generic, Iterable
from uuid import UUID

from pydantic import BaseModel

from app.core.pagination.page import Page
from app.features.storage.services.sotrage_service import StorageService

EntityT = TypeVar("EntityT")
ResponseT = TypeVar("ResponseT", bound=BaseModel)


class ResponseFactory(Generic[EntityT, ResponseT]):
    def __init__(self, storage: StorageService):
        self._storage = storage

    def create(self, entity: EntityT) -> ResponseT:
        raise NotImplementedError

    def create_many(self, entities: Iterable[EntityT]) -> list[ResponseT]:
        return [self.create(entity) for entity in entities]

    def create_page(self, page: Page[EntityT]) -> Page[ResponseT]:
        return page.map(self.create)

    def file_url(self, file_id: UUID | None) -> str | None:
        return self._storage.public_url(file_id)
