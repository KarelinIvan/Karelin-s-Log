from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers.router import pages_router as router
from app.core.templates import templates
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.schemas.post import PostUpdate
from app.services.blog_service import BlogService
from app.services.exceptions import PostNotFoundError


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request, page: int = 1, session: AsyncSession = Depends(get_session)
):
    """
    Главная страница со списком постов.
    Реализована постраничная пагинация (10 постов).
    """
    repo = PostRepository(session)
    service = BlogService(repo)

    limit = 10
    # расчёт смещения
    skip = (page - 1) * limit

    posts = await service.get_posts(skip=skip, limit=limit)
    total_posts = await service.count_posts()

    # Расчитываем общее количество страниц (округляем вверх)
    total_pages = (total_posts + limit - 1) // limit

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts, "page": page, "total_pages": total_pages},
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


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_page(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Страница редактирования поста."""
    repo = PostRepository(session)
    service = BlogService(repo)

    try:
        post = await service.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return templates.TemplateResponse(
        request=request, name="edit_post.html", context={"post": post}
    )


@router.post("/posts/{post_id}/edit")
async def edit_post_action(
    post_id: int,
    title: str = Form(),
    description: str = Form(),
    published: bool = Form(False),
    session: AsyncSession = Depends(get_session),
):
    """Обрабатывает форму редактирования поста."""
    repo = PostRepository(session)
    service = BlogService(repo)

    update_data = PostUpdate(title=title, description=description, published=published)

    try:
        await service.update_post(post_id, update_data)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return RedirectResponse(url=f"/page/posts/{post_id}", status_code=303)


@router.post("/posts/{post_id}/delete")
async def delete_post_action(
    post_id: int, session: AsyncSession = Depends(get_session)
):
    """Удаляет пост и перенаправляет на главную страницу."""
    repo = PostRepository(session)
    service = BlogService(repo)

    try:
        await service.delete_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return RedirectResponse(url="/page/", status_code=303)
