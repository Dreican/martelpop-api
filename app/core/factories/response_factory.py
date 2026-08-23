from typing import TypeVar, Generic, Iterable
from uuid import UUID

from pydantic import BaseModel

from app.core.config.configuration import get_config
from app.core.pagination.page import Page

EntityT = TypeVar("EntityT")
ResponseT = TypeVar("ResponseT", bound=BaseModel)

config = get_config()
FILE_URL_PREFIX = f"{config.app.api_prefix}/files"


class ResponseFactory(Generic[EntityT, ResponseT]):

    def create(self, entity: EntityT) -> ResponseT:
        raise NotImplementedError

    def create_many(self, entities: Iterable[EntityT]) -> list[ResponseT]:
        return [self.create(entity) for entity in entities]

    def create_page(self, page: Page[EntityT]) -> Page[ResponseT]:
        return page.map(self.create)

    @staticmethod
    def file_url(file_id: UUID | None) -> str | None:
        if file_id is None:
            return None

        return f"{FILE_URL_PREFIX}/{file_id}"
