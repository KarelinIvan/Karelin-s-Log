from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

import app.core.settings
import app.models

# Асинхронный движок
engine = create_async_engine(
    url=app.core.settings.settings.DATABASE_URL,
    echo=app.core.settings.settings.DEBUG_SQLALCHEMY,
    pool_pre_ping=True,  # Проверяет соединение перед использованием
)

# Фабрика асинхронных сессий для CRUD-операций через ORM
# Отключаем expire_on_commit (по умолчанию флаг True),
# чтобы объекты оставались валидными и готовыми к использованию
session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """
    Создаёт таблицы в базе данных на основании моделей,
    унаследованных от SQLModel, у которых флаг table=True.
    """
    async with engine.begin() as connect:
        await connect.run_sync(SQLModel.metadata.create_all)
