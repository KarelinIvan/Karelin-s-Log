import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.session import get_session
from app.main import app
from app.models.post import Post


@pytest.fixture
async def sample_post(test_session):
    """Фикстура создает пост в таблице posts"""
    post = Post(title="Заголовок теста", description="Тестовое описание")
    test_session.add(post)
    await test_session.commit()
    await test_session.refresh(post)
    yield post


@pytest.fixture
async def async_client(test_engine):
    """Создаёт HTTP-клиент с подменой зависимости БД на тестовую."""
    # Создаём фабрику сессии
    test_sessionmaker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,  # ← класс из SQLModel
        expire_on_commit=False,
    )

    # Создаём функцию-заменитель get_session
    async def override_get_session():
        async with test_sessionmaker() as session:
            yield session

    # Подменяем зависимость
    app.dependency_overrides[get_session] = override_get_session
    # Создаём клиент и отдаем тесту
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # Очищаем подмену после теста
    app.dependency_overrides.clear()
