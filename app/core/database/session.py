from functools import lru_cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine

from app.core.config.configuration import get_config


@lru_cache
def get_engine() -> AsyncEngine:
    config = get_config()

    return create_async_engine(
        config.db.database_url,
        echo=config.app.debug,
        pool_pre_ping=True
    )


@lru_cache
def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )
