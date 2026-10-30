from fastapi import Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers import post  # noqa: F401, PLW0406
from app.controllers.router import router
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.blog_service import BlogService
from app.services.exceptions import (
    PostNotFoundError,
    TitleAlreadyExistsError,
    TitleEmptyError,
)


@router.post("/", response_model=PostRead, status_code=201)
async def create_post(
    data: PostCreate,
    session: AsyncSession = Depends(get_session),
) -> PostRead:
    """Создаёт новый пост в базе данных."""
    repo = PostRepository(session)
    service = BlogService(repo)
    try:
        post = await service.create_post(data)
    except TitleEmptyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except TitleAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return post  # type: ignore


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
) -> PostRead:
    """Находит пост в базе данных по ID."""
    repo = PostRepository(session)
    service = BlogService(repo)
    try:
        post = await service.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return post  # type: ignore


@router.get("/", response_model=list[PostRead])
async def get_posts(
    session: AsyncSession = Depends(get_session),
) -> list[PostRead]:
    """Возвращает список всех постов"""
    repo = PostRepository(session)
    service = BlogService(repo)

    posts = await service.get_posts()
    return posts  # type: ignore


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int, data: PostUpdate, session: AsyncSession = Depends(get_session)
) -> PostRead:
    """Обновляет пост частичными данными."""
    repo = PostRepository(session)
    service = BlogService(repo)

    try:
        post = await service.update_post(post_id, data)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return post  # type: ignore
