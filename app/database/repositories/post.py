from sqlmodel.ext.asyncio.session import AsyncSession, select

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
