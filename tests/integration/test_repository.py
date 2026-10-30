from sqlmodel import select

from app.database.repositories.post import PostRepository
from app.models.post import Post
from app.schemas.post import PostCreate


async def test_repository_create(test_session):
    """
    Тест создает новый пост в базе данных.
    Проверяет, что посту присвоено ID.
    Проверяет, что все поля заполнены верно.
    """
    repo = PostRepository(test_session)
    data = PostCreate(
        title="Тестовый заголовок",
        description="Описание",
    )
    post = await repo.create(data)

    # Проверяем присвоение id
    assert post.id is not None

    # Проверяем данные
    result = await test_session.exec(select(Post).where(Post.id == post.id))
    found = result.one()
    assert found.title == data.title
    assert found.description == data.description
    assert found.published is False


async def test_repository_get_by_id(test_session, sample_post):
    """Тест проверяет поиск постов по ID в репозитории."""
    repo = PostRepository(test_session)

    # Ищем существующий пост (из фикстуры)
    found = await repo.get_by_id(sample_post.id)

    # Проверяем, что книга найдена и совпадает по ID
    assert found is not None
    assert found.id == sample_post.id

    # Проверяем, что несуществующий ID возвращает None
    missing_post = await repo.get_by_id(9999)
    assert missing_post is None
