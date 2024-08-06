import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from config import Config
from exceptions import CustomSqlAlchemyException

logger = logging.getLogger(__name__)


async_engine = create_async_engine(
    Config.DATABASE_URL,
    poolclass=NullPool,
    # echo=Config.ECHO_SQL, # To show the debug log in terminal
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    """
    Dependency function that yields db async sessions.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exc:
            # Transaction failed
            msg = f"SQLAlchemyError happened in the session dependency: {repr(exc)}"
            await session.rollback()
            logger.exception(msg)
            # NOTE: For custom exc handling to work here, consider wrapping into middleware
            raise CustomSqlAlchemyException(msg)
