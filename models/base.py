from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


from . import get_database_token

engine = create_async_engine(get_database_token())
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


async def async_create() -> None: # --> создание БД + таблицы
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def async_drop() -> None: # --> удаление всех таблиц полностью
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
    await engine.dispose()

