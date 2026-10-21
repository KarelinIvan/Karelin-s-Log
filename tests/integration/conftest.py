import pytest

from app.models.post import Post


@pytest.fixture
async def sample_post(test_session):
    """Фикстура создает пост в таблице posts"""
    post = Post(title="Заголовок теста", description="Тестовое описание")
    test_session.add(post)
    await test_session.commit()
    await test_session.refresh(post)
    yield post
