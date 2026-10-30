from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Post
from app.schemas.post import PostCreate


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PostCreate) -> Post:
        """
        Создает новы пост в базе данных
        Args:
            data (PostCreate): Валидированные данные поста
            (title, description, published).

        Returns:
            Post: ORM-объект с присвоенным id и заполненными created_at,
            updated_at.
        """
        post = Post(
            title=data.title,
            description=data.description,
            published=data.published,
        )
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_by_title(self, title: str) -> Post | None:
        """
        Ищет пост по заголовку.
        Возвращает Post или None, если не найден.
        """
        result = await self.session.exec(select(Post).where(Post.title == title))
        return result.first()

    async def get_by_id(self, post_id: int) -> Post | None:
        """
        Метод ищет пост по id.
        Возвращает Post или None, если не найден.
        """
        result = await self.session.exec(select(Post).where(Post.id == post_id))
        return result.first()

    async def get_all(self) -> list[Post]:
        """Метод возвращает все посты из базы данных."""
        result = await self.session.exec(select(Post))
        return list(result.all())

    async def update(self, post: Post, data: dict) -> Post:
        """
        Метод обновляет поля поста и сохраняет изменения в базу данных.
        Обновляются только те поля, которые прислал пользователь,
        остальные поля остаются без изменений.

        Args:
            post: ORM-объект поста.
            data: Словарь с полями для обновления.

        Returns:
            Post: Обновлённый пост.
        """
        # Применяем изменения к объекту
        for key, value in data.items():
            setattr(post, key, value)

        self.session.add(post)

        await self.session.commit()
        await self.session.refresh(post)

        return post
