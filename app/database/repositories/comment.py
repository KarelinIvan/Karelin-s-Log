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

        return list(result.scalars().all())

    async def get_tree_by_post_id(self, post_id: int) -> list[Comment]:
        """
        Возвращает дерево комментариев поста.
        Список корневых комментариев (parent_id is None); у каждого есть
        атрибут .replies — список прямых ответов
        """

        all_comments = await self.get_by_post_id(post_id)

        # Ключ словаря строго int, так как группируется только те у которых parent_id не None
        replies_by_parent: dict[int, list[Comment]] = {}
        for comment in all_comments:
            if comment.parent_id is not None:
                replies_by_parent.setdefault(comment.parent_id, []).append(comment)

        root_comments: list[Comment] = []
        for comment in all_comments:
            if comment.parent_id is None:
                # Утверждаем для Pylance/mypy, что id у корневого комментария есть
                assert comment.id is not None
                comment.replies = replies_by_parent.get(comment.id, [])
                root_comments.append(comment)

        return root_comments

    async def get_by_id(self, comment_id: int) -> Comment | None:
        """
        Возвращает комментарий.

        Returns:
            Возвращает комментарий.
        """
        result = await self.session.exec(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.first()
