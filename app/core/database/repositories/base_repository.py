from typing import TypeVar
from uuid import UUID

from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.base import Base
from app.core.exceptions.base import ApplicationError
from app.core.pagination.page import Page
from app.core.pagination.page_request import PageRequest

T = TypeVar("T", bound=Base)


class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: type[T], not_found_exception: type[ApplicationError]):
        self._session = session
        self._model = model
        self._not_found_exception = not_found_exception

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)

    async def get_by_id(self, entity_id: UUID) -> T | None:
        stmt = select(self._model).where(self._model.id == entity_id)
        return await self._session.scalar(stmt)

    async def get_required(self, entity_id: UUID) -> T:
        entity = await self.get_by_id(entity_id)

        if entity is None:
            raise self._not_found_exception(entity_id=entity_id)

        return entity

    async def paginate(self, stmt: Select[tuple[T]], request: PageRequest) -> Page[T]:
        total_stmt = (
            select(func.count())
            .select_from(stmt.order_by(None).subquery())
        )

        total = await self._session.scalar(total_stmt)
        if total is None:
            total = 0

        stmt = (stmt.offset(request.offset).limit(request.page_size))

        items = list(await self._session.scalars(stmt))

        return Page(items=items, page=request.page, page_size=request.page_size, total=total)
