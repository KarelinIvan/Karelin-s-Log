from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Comment
from app.schemas.comment import CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        """Сохраняет сессию."""
        self.session = session

    async def create(
        self, data: CommentCreate, post_id: int, parent_id: int | None = None
    ) -> Comment:
        """
        Создаёт новый комментарий в базе данных.

        Args:
            data (CommentCreate): Валидные данные комментария.
            post_id (int): ID поста к которым принадлежит комментарий.
            parent_id (int | None): Ссылка на родительский комментарий.

        Returns:
                Comment: ORM-объект с присвоенным id и заполненными created_at.
        """
        comment = Comment(
            author_name=data.author_name,
            text=data.text,
            email=data.email,
            post_id=post_id,
            parent_id=parent_id,
        )
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_post_id(self, post_id: int) -> list[Comment]:
        """
        Возвращает список комментариев.

        Returns:
            Возвращает отсортированный по дате создания список комментариев
            принадлежащий посту.
        """
        result = await self.session.exec(
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(col(Comment.created_at).asc())
        )
        return list(result.all())
