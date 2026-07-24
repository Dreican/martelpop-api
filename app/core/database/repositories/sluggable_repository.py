from typing import Protocol, TypeVar

from sqlalchemy import select

from app.core.database.repositories.base_repository import BaseRepository


class HasSlug(Protocol):
    slug: str


TSlug = TypeVar("TSlug", bound=HasSlug)


class SluggableRepository[T](BaseRepository[T]):

    async def exists_by_slug(self, slug: str) -> bool:
        stmt = select(self._model).where(self._model.slug == slug)
        return await self._session.scalar(stmt) is not None

    async def get_by_slug(self, slug: str) -> TSlug | None:
        stmt = select(self._model).where(self._model.slug == slug)
        return await self._session.scalar(stmt)

    async def required_by_slug(self, slug: str) -> T:
        entity  = await self.get_by_slug(slug)

        if entity  is None:
            raise self._not_found_exception()

        return entity