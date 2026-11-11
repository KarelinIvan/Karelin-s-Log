from unittest.mock import AsyncMock

from app.services.comment_service import CommentService


async def test_comment_service_get_comments_returns_repo_data():
    """
    Юнит-тест: проверяет, что сервис просто возвращает то,
    что ему отдал репозиторий (без реальной базы данных).
    """
    # Создаём фейковый репозиторий
    mock_repo = AsyncMock()

    fake_comments = ["Комментарий один", "Комментарий два"]
    mock_repo.get_by_post_id.return_value = fake_comments
    comment_service = CommentService(repo=mock_repo)

    result = await comment_service.get_comments(post_id=42)
    assert result == fake_comments
    mock_repo.get_by_post_id.assert_awaited_once_with(42)


async def test_get_comment_by_id_returns_none_when_not_found():
    """
    Юнит-тест: проверяет, что если комментарий не найден, сервис возвращает None.
    """
    mock_repo = AsyncMock()

    mock_repo.get_by_id.return_value = None
    comment_service = CommentService(repo=mock_repo)

    result = await comment_service.get_comment_by_id(comment_id=99)
    assert result is None
    mock_repo.get_by_id.assert_awaited_once_with(99)
