from app.database.repositories.post import PostRepository
from app.schemas.post import PostCreate
from app.services.blog_service import BlogService


async def test_service_create_post(test_session):
    """Тест проверяет успешное создание поста через сервис."""
    repo = PostRepository(test_session)
    service = BlogService(repo)
    data = PostCreate(title="Новый пост", description="Описание")
    post = await service.create_post(data)

    assert post.id is not None
    assert post.title == data.title
    assert post.description == data.description
    assert post.published is False
