from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

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
session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Используется в тестах (tests/integration/test_db_tables.py)
# для проверки создания таблиц. В проде схема управляется через Alembic.
async def create_db_and_tables(db_engine):
    """
    Создаёт таблицы в базе данных на основании моделей,
    унаследованных от SQLModel, у которых флаг table=True.
    """
    async with db_engine.begin() as connect:
        await connect.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Зависимость FastAPI: отдаёт сессию БД на время запроса."""
    async with session() as db_session:
        yield db_session
