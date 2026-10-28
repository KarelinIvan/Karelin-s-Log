from app.database.repositories.post import PostRepository
from app.models.post import Post
from app.schemas.post import PostCreate
from app.services.exceptions import (
    PostNotFoundError,
    TitleAlreadyExistsError,
    TitleEmptyError,
)


class BlogService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def create_post(self, data: PostCreate) -> Post:
        """
        Создаёт новый пост, проверяя бизнес-правила.

        Args:
            data: Валидированные данные поста (title, description, published).

        Returns:
            Post: Созданный пост с присвоенным id и временными метками.

        Raises:
            TitleEmptyError: Если title пустой или состоит только из пробелов.
            TitleAlreadyExistsError: Если пост с таким title уже существует.
        """
        if not data.title or not data.title.strip():
            raise TitleEmptyError("Title не может быть пустым")
        if await self.repo.get_by_title(data.title):
            raise TitleAlreadyExistsError("Пост с таким title уже существует")
        return await self.repo.create(data)

    async def get_post(self, post_id: int) -> Post:
        """
        Находит пост по его id.

        Args:
            post_id (int): ID поста.

        Returns:
            Post: Найден пост.

        Raises:
            PostNotFoundError: Если пост не найден.
        """
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise PostNotFoundError(f"Пост с id: {post_id} не найден")
        return post
