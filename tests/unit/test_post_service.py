from unittest.mock import AsyncMock

import pytest

from app.schemas.post import PostCreate
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
