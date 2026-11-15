from sqlalchemy import case
from sqlmodel import col, func, or_, select
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

    async def get_all(
        self, skip: int = 0, limit: int = 10, published: bool | None = None
    ) -> list[Post]:
        """
        Метод возвращает список постов с пагинацией и сортирует его по дате публикации.
        Отображает опубликованные посты и черновики.

        Args:
            skip (int): Сколько записей пропустить.
            limit (int): Сколько записей вернуть (по умолчанию 10).
            published (bool | None): Фильтр по статусу: True — опубликованные,
                False — черновики, None — все посты».
        Returns:
            list[Post]: Возвращает список постов.
        """
        query = select(Post)

        if published is not None:
            query = query.where(Post.published == published)

        result = await self.session.exec(
            query.order_by(col(Post.published_at).desc()).offset(skip).limit(limit)
        )
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

    async def delete(self, post: Post) -> None:
        """
        Метод удаляет пост из базы данных.

        Args:
            post (Post): ORM-объект пост (уже найден и привязан к сессии).
        """
        await self.session.delete(post)
        await self.session.commit()

    async def count(self, published: bool | None = None) -> int:
        """
        Метод возвращает количество постов в базе данных.

        Returns:
            int: Количество постов.
        """
        query = select(func.count()).select_from(Post)

        if published is not None:
            query = query.where(Post.published == published)

        result = await self.session.exec(query)
        return result.one()

    async def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Post]:
        """
        Метод возвращает список постов из базы данных, при посике по заголовку или описанию.
        """

        statement = select(Post).where(
            or_(Post.title.ilike(f"%{query}%"), Post.description.ilike(f"%{query}%"))
        )

        # Приоритет поиска по совпалениям
        priority = case(
            (col(Post.title) == query, 1),  # Заголовок полностью совпадает с запросом
            (col(Post.title).ilike(f"{query}%"), 2),  # совпадение в начале заголовка
            (col(Post.title).ilike(f"%{query}%"), 3),  # совпадение в середине заголовка
            else_=4,  # совпадение только в описании
        )

        request = await self.session.exec(
            statement.order_by(priority).offset(skip).limit(limit)
        )
        return list(request.all())
