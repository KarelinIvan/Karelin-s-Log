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
