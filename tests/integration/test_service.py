import pytest

from app.database.repositories.post import PostRepository
from app.schemas.post import PostCreate
from app.services.blog_service import BlogService
from app.services.exceptions import (
    PostNotFoundError,
    TitleAlreadyExistsError,
    TitleEmptyError,
)


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


async def test_title_empty_error(test_session):
    """Тест проверяет, что сервис бросает TitleEmptyError при пустом title."""
    repo = PostRepository(test_session)
    service = BlogService(repo)
    data = PostCreate(title="", description="Описание")

    with pytest.raises(TitleEmptyError):
        await service.create_post(data)


async def test_title_already_exists_error(test_session, sample_post):
    """
    Тест проверяет, что сервис бросает TitleAlreadyExistsError
    при занятом title.
    """
    repo = PostRepository(test_session)
    service = BlogService(repo)
    data = PostCreate(title=sample_post.title, description="Описание")

    with pytest.raises(TitleAlreadyExistsError):
        await service.create_post(data)


async def test_service_get_post(test_session, sample_post):
    """Тест проверяет успешное получение поста через сервис."""
    repo = PostRepository(test_session)
    service = BlogService(repo)

    post = await service.get_post(sample_post.id)

    assert post is not None
    assert post.id == sample_post.id


async def test_service_get_post_not_found(test_session):
    """Тест проверяет ошибку PostNotFoundError, если поста нет."""
    repo = PostRepository(test_session)
    service = BlogService(repo)

    with pytest.raises(PostNotFoundError):
        await service.get_post(9999)
