from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.templates import templates
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.services.blog_service import BlogService
from app.services.exceptions import PostNotFoundError

router = APIRouter(prefix="/page", tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, session: AsyncSession = Depends(get_session)):
    """Главная страница со списком постов."""
    repo = PostRepository(session)
    service = BlogService(repo)

    posts = await service.get_posts(limit=10)

    return templates.TemplateResponse(
        request=request, name="index.html", context={"posts": posts}
    )


@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Страница с деталями поста."""
    repo = PostRepository(session)
    service = BlogService(repo)

    try:
        post = await service.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return templates.TemplateResponse(
        request=request, name="post_detail.html", context={"post": post}
    )
