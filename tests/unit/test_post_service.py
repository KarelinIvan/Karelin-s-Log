from turtle import title
from unittest import mock
from unittest.mock import AsyncMock

import pytest

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.services.exceptions import TitleEmptyError
from app.services.post_service import PostService


async def test_title_empty_error():
    """
    Юнит-тест: проверяет, что при создании поста с пустым заголовком сервис
    выбрасывает ошибку TitleEmptyError и не передаёт данные в репозиторий.
    """
    mock_repo = AsyncMock()
    service = PostService(repo=mock_repo)
    data = PostCreate(title=" ", description="Описание")

    with pytest.raises(TitleEmptyError):
        await service.create_post(data)

    mock_repo.create.assert_not_awaited()


async def test_update_post_sets_published_at_on_first_publish():
    """
    Юнит-тест: проверяет, что сервис автоматически ставит дату публикации,
    когда пост публикуется впервые.
    """
    mock_repo = AsyncMock()
    fake_post = Post(
        id=100, title="Заголовок", description="Описание", published_at=None
    )
    mock_repo.get_by_id.return_value = fake_post
    service = PostService(repo=mock_repo)
    data = PostUpdate(published=True)
    await service.update_post(100, data)

    mock_repo.update.assert_awaited_once()
    update_data = mock_repo.update.call_args[0][1]

    assert "published_at" in update_data
    assert update_data["published_at"] is not None
