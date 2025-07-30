from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from models import async_session

async def get_connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise