from app.database.repositories.comment import CommentRepository
from app.models import Comment
from app.schemas.comment import CommentCreate


class CommentService:
    def __init__(self, repo: CommentRepository):
        """Сохраняет репозиторий."""
        self.repo = repo

    async def create_comment(self, data: CommentCreate, post_id: int) -> Comment:
        """
        Принимает валидные данные и возвращает результат.

        Args:
            data (CommentCreate): Валидированные данные комментария.
            post_id (int): ID поста которому принадлежит комментарий.
        Returns:
            Comment: Созданный комментарий с присвоенным id и временными метками.
        """
        return await self.repo.create(data, post_id)

    async def get_comments(self, post_id: int) -> list[Comment]:
        """
        Возвращает список комментариев для поста.

        Args:
            post_id (int): ID поста которому принадлежит комментарий.
        Returns:
            list[Comment]: Возвращает список комментариев.`
        """
        return await self.repo.get_by_post_id(post_id)
