import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import text

from app.database.session import create_db_and_tables
from app.models import Post  # noqa: F401 — регистрирует Post в SQLModel.metadata


async def test_create_db_and_tables(test_engine):
    """
    Тест проверяет создание таблицы posts в базе данных.
    Сначала выполняется очистка перед тестом.
    После этого создается новая таблица posts и тест проверяет,
    создана ли таблица в базе данных или нет.
    """

    # Очистка перед тестом
    async with test_engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS posts CASCADE"))

    # Вызов функции
    try:
        await create_db_and_tables(db_engine=test_engine)
    except SQLAlchemyError as e:
        pytest.fail(f"Не удалось создать таблицу 'posts' в базе данных: {e}")

    # Проверка
    async with test_engine.connect() as conn:
        result = await conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = 'posts'"
            )
        )
    assert result.scalar() == "posts", "Таблица 'posts' не была создана"
