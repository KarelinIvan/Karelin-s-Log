from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Post
from app.schemas.post import PostCreate


class PostRepositiry:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PostCreate) -> Post:  # pyright: ignore[reportReturnType]
        post = Post(
            title=data.title,
            description=data.description,
            published=data.published,
        )
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
