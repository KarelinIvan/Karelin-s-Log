import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import text


async def test_db_connection(test_engine):
    """Тест проверяет подключение к базе данных."""
    try:
        async with test_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        pytest.fail(f"Не удалось подключиться к PostgreSQL: {e}")
    assert result.scalar() == 1
