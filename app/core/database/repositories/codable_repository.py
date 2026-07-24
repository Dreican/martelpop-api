from enum import StrEnum
from typing import Protocol, TypeVar, Generic

from sqlalchemy import select

from app.core.database.repositories.base_repository import BaseRepository


class HasCode(Protocol):
    code: StrEnum


EntityT = TypeVar("EntityT")
CodeT = TypeVar("CodeT", bound=StrEnum)


class CodableRepository(BaseRepository[EntityT], Generic[EntityT, CodeT]):

    async def get_by_code(self, code: CodeT) -> EntityT | None:
        stmt = select(self._model).where(self._model.code == code)
        return await self._session.scalar(stmt)

    async def exists_by_code(self, code: CodeT) -> bool:
        stmt = select(self._model).where(self._model.code == code)
        return await self._session.scalar(stmt) is not None

    async def require_by_code(self, code: CodeT) -> EntityT:
        stmt = select(self._model).where(self._model.code == code)
        entity = await self._session.scalar(stmt)
        if entity is None:
            raise self._not_found_exception(code)
        return entity
