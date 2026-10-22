import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Post

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture
async def test_engine():
    """
    Фикстура проверяет, что TEST_DATABASE_URL задан и указывает на тестовую БД
    (иначе pytest.fail). Затем создаёт engine, выполняет create_all для создания
    таблиц и отдаёт engine тесту.

    yield приостанавливает фикстуру до окончания теста.
    После теста dispose() освобождает пул соединений (даже если тест упал).
    """
    url = TEST_DATABASE_URL
    if not url:
        pytest.fail("TEST_DATABASE_URL не задан")
    if "_test" not in url:
        pytest.fail("URL не похож на тестовую базу данных")
    # создаем тестовый движок
    engine = create_async_engine(url)

    async with engine.begin() as connect:
        await connect.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """
    Фикстура создаёт фабрику сессий и отдаёт тестовую сессию тесту
    Контекстный менеджер открывает сессию.
    Выполняется удаление постов и делается коммит,
    после этого yield передает сессию тесту и присотанавливает фикстуру.

    """
    sessionmaker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with sessionmaker() as session:
        await session.exec(delete(Post))
        await session.commit()
        yield session
