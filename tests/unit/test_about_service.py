from unittest.mock import AsyncMock

from app.models.about import About
from app.services.about_service import AboutService


async def test_about_service_update():
    """Юнит-тест: проверяет, что метод update сервиса передает данные в репозиторий."""
    mock_repo = AsyncMock()
    about_service = AboutService(mock_repo)

    fake_about = About(content="Текст" * 30)

    mock_repo.update.return_value = fake_about

    result = await about_service.update(fake_about, {"content": "Новый текст" * 20})
    assert result == fake_about
    mock_repo.update.assert_awaited_once_with(
        fake_about, {"content": "Новый текст" * 20}
    )
