import logging
from typing import Any

from sqlalchemy import select, Select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.helpers import Helper
from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.core.pagination.page import Page
from app.features.auth.exceptions.authentication_exceptions import EmailAlreadyExistsError
from app.features.auth.models.role import Role
from app.features.users.dto.user_search_request import UserSearchRequest
from app.features.users.enums.user_sort import UserSort
from app.features.users.exceptions.user_exceptions import UserNotFoundError
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class UserRepository(SluggableRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User, not_found_exception=UserNotFoundError)

    async def add(self, entity: User) -> None:
        try:
            await super().add(entity)
            await self._session.flush()
        except IntegrityError as ex:
            if Helper.is_email_unique_violation(ex):
                logger.debug("Email already exists, unique constraint violation")
                raise EmailAlreadyExistsError(email=entity.email) from ex
            raise

    async def search(self, request: UserSearchRequest) -> Page[User]:
        stmt = select(User)

        stmt = self._apply_filters(stmt, request)
        stmt = self._apply_sort(stmt, request.sort)

        return await self.paginate(stmt, request.pagination)


    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User).where(User.email == email)
        )

        return await self._session.scalar(stmt)

    async def get_by_email_with_identities(self, email: str) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.authentication_identities))
            .where(User.email == email)
        )

        return await self._session.scalar(stmt)

    async def exists_by_email(self, email: str) -> bool:
        stmt = (
            select(User).where(User.email == email)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    def _apply_filters(stmt: Select[tuple[Any]], request: UserSearchRequest) -> Select[tuple[Any]]:
        if request.query:
            stmt = stmt.where(
                or_(
                    User.display_name.ilike(f"%{request.query}%"),
                    User.email.ilike(f"%{request.query}%"),
                    User.firstname.ilike(f"%{request.query}%"),
                    User.lastname.ilike(f"%{request.query}%")
                )
            )

        if request.role:
            stmt = stmt.where(Role.code.in_(request.role))

        if request.status:
            stmt = stmt.where(User.status.in_(request.status))


        return stmt


    @staticmethod
    def _apply_sort(stmt: Select[tuple[Any]], sort: UserSort) -> Select[tuple[Any]]:
        sorts = {
            UserSort.CREATED_AT_ASC: User.created_at.asc(),
            UserSort.CREATED_AT_DESC: User.created_at.desc(),
            UserSort.DISPLAY_NAME_ASC: User.display_name.asc(),
            UserSort.DISPLAY_NAME_DESC: User.display_name.desc(),
            UserSort.EMAIL_ASC: User.email.asc(),
            UserSort.EMAIL_DESC: User.email.desc(),
            UserSort.FULLNAME_ASC: User.display_name.asc(),
            UserSort.FULLNAME_DESC: User.display_name.desc(),
            UserSort.ROLE_ASC: User.role.asc(),
            UserSort.ROLE_DESC: User.role.desc(),
            UserSort.STATUS_ASC: User.status.asc(),
            UserSort.STATUS_DESC: User.status.desc(),
        }

        stmt = stmt.order_by(
            sorts.get(
                sort,
                User.created_at.desc(),
            )
        )

        return stmt