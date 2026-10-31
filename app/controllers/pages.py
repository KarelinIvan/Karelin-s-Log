from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.templates import templates
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.services.blog_service import BlogService

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, session: AsyncSession = Depends(get_session)):
    """Главная страница со списком постов."""
    repo = PostRepository(session)
    service = BlogService(repo)

    posts = await service.get_posts(limit=10)

    return templates.TemplateResponse(
        request=request, name="index.html", context={"posts": posts}
    )
