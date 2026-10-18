import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture
async def test_engine():
    """
    Фикстура проверяет задал ли путь к тестовой базе данных, в случае ошибки
    fail() проваливает тест.
    После проверки пути, создается тестовый движок.
    Оператор yield, отдаёт обращение(engine) и приостонавливает фикстуру до
    окончания теста.
    После окнчания теста dispose() закрывает пул и свободные соединения
    (даже если тест упал).
    """
    url = TEST_DATABASE_URL
    if not url:
        pytest.fail("TEST_DATABASE_URL не задан")
    if "_test" not in url:
        pytest.fail("URL не похож на тестовую базу данных")
    # создаем тестовый движок
    engine = create_async_engine(url)
    yield engine
    await engine.dispose()
