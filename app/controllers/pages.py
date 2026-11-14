from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers.router import pages_router as router
from app.core.settings import settings
from app.core.templates import templates
from app.database.repositories.about import AboutRepository
from app.database.repositories.comment import CommentRepository
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.schemas.comment import CommentCreate
from app.schemas.post import PostUpdate
from app.services.about_service import AboutService
from app.services.comment_service import CommentService
from app.services.exceptions import PostNotFoundError
from app.services.post_service import PostService

serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="admin-session")


def get_current_user(request: Request) -> str | None:
    """
    Возвращает имя авторизованного пользователя из куки.

    Args:
        request: HTTP-запрос, из которого читается кука.
    Returns:
        str | None: Имя пользователя ("admin"), если кука валидна,
                    иначе None (не авторизован или сессия истекла).
    """
    token = request.cookies.get("admin_session")
    if not token:
        return None

    try:
        data = serializer.loads(token, max_age=3600)
        return data.get("user")
    except (BadSignature, SignatureExpired):
        return None


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request, page: int = 1, session: AsyncSession = Depends(get_session)
):
    """
    Главная страница со списком постов.
    Реализована постраничная пагинация (10 постов).
    Отображает только опубликованные посты published=True.
    Передаёт в шаблон информацию о текущем пользователе
    (для отображения приветствия или ссылки "Авторизоваться").
    """
    post_repo = PostRepository(session)
    post_service = PostService(post_repo)

    limit = 10
    # расчёт смещения
    skip = (page - 1) * limit

    posts = await post_service.get_posts(skip=skip, limit=limit, published=True)
    total_posts = await post_service.count_posts(published=True)

    # Расчитываем общее количество страниц (округляем вверх)
    total_pages = (total_posts + limit - 1) // limit

    current_user = get_current_user(request)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "posts": posts,
            "page": page,
            "total_pages": total_pages,
            "current_user": current_user,
        },
    )


@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Страница с деталями поста.
    Передаёт в шаблон информацию о текущем пользователе
    (для отображения приветствия или ссылки "Авторизоваться").
    """
    post_repo = PostRepository(session)
    post_service = PostService(post_repo)

    comment_repo = CommentRepository(session)
    comment_service = CommentService(comment_repo)

    try:
        post = await post_service.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    comments = await comment_service.get_comments(post_id)

    current_user = get_current_user(request)

    return templates.TemplateResponse(
        request=request,
        name="post_detail.html",
        context={
            "post": post,
            "current_user": current_user,
            "comments": comments,
            "admin_name": settings.ADMIN_NAME,
        },
    )


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_page(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Страница редактирования поста.
    Передаёт в шаблон информацию о текущем пользователе
    (для отображения приветствия или ссылки "Авторизоваться").
    """
    post_repo = PostRepository(session)
    post_service = PostService(post_repo)

    try:
        post = await post_service.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    current_user = get_current_user(request)

    return templates.TemplateResponse(
        request=request,
        name="edit_post.html",
        context={"post": post, "current_user": current_user},
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
    post_repo = PostRepository(session)
    post_service = PostService(post_repo)

    update_data = PostUpdate(title=title, description=description, published=published)

    try:
        await post_service.update_post(post_id, update_data)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return RedirectResponse(url=f"/page/posts/{post_id}", status_code=303)


@router.post("/posts/{post_id}/delete")
async def delete_post_action(
    post_id: int, session: AsyncSession = Depends(get_session)
):
    """Удаляет пост и перенаправляет на главную страницу."""
    post_repo = PostRepository(session)
    post_service = PostService(post_repo)

    try:
        await post_service.delete_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return RedirectResponse(url="/page/", status_code=303)


@router.post("/posts/{post_id}/comments")
async def post_comment_action(
    post_id: int,
    author_name: str = Form(),
    text: str = Form(),
    email: str = Form(),
    session: AsyncSession = Depends(get_session),
):
    """Обрабатывает форму записи комментариев."""
    comment_repo = CommentRepository(session)
    comment_service = CommentService(comment_repo)

    data = CommentCreate(author_name=author_name, text=text, email=email)
    await comment_service.create_comment(data, post_id)
    return RedirectResponse(url=f"/page/posts/{post_id}", status_code=303)


@router.post("/comments/{comment_id}/reply")
async def post_comment_reply(
    comment_id: int, text: str = Form(), session: AsyncSession = Depends(get_session)
):
    """Обрабатывает форму для ответа на комментарии."""
    comment_repo = CommentRepository(session)
    comment_service = CommentService(comment_repo)

    parent_comment = await comment_service.get_comment_by_id(comment_id)

    if parent_comment is None:
        raise HTTPException(status_code=404, detail="Комментарий отсутствует")

    data = CommentCreate(
        author_name=settings.ADMIN_NAME, text=text, email=settings.ADMIN_EMAIL
    )

    await comment_service.create_comment(
        data, parent_comment.post_id, parent_id=comment_id
    )
    return RedirectResponse(
        url=f"/page/posts/{parent_comment.post_id}", status_code=303
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, session: AsyncSession = Depends(get_session)):
    """Страница отображения информации 'Обо мне'."""
    about_repo = AboutRepository(session)
    about_service = AboutService(about_repo)

    about = await about_service.get()

    current_user = get_current_user(request)

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={"current_user": current_user, "about": about},
    )
