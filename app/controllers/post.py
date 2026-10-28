from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers import post  # noqa: F401, PLW0406
from app.controllers.router import router
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.schemas.post import PostCreate, PostRead
from app.services.blog_service import BlogService
from app.services.exceptions import TitleAlreadyExistsError, TitleEmptyError


@router.post("/", response_model=PostRead, status_code=201)
async def create_post(
    data: PostCreate,
    session: AsyncSession = Depends(get_session),
):
    repo = PostRepository(session)
    service = BlogService(repo)
    try:
        post = await service.create_post(data)
    except TitleEmptyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except TitleAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return post
