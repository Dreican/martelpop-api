from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.dependencies.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.db.database_url,
    echo=settings.app.debug,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)
