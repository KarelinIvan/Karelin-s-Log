from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers.dependencies import password_hash
from app.controllers.router import admin_router as router
from app.controllers.router import auth_router
from app.core.settings import settings
from app.core.templates import templates
from app.database.repositories.post import PostRepository
from app.database.session import get_session
from app.schemas.post import PostCreate
from app.services.blog_service import BlogService
from app.services.exceptions import TitleAlreadyExistsError, TitleEmptyError

serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="admin_session")


@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    """Тестовая страница админки."""
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={"message": "Админка работает!"},
    )


@router.get("/posts/create", response_class=HTMLResponse)
async def create_post_page(request: Request):
    """Страница создания нового поста."""
    return templates.TemplateResponse(request=request, name="admin/create_post.html")


@router.post("/posts/create")
async def create_post_action(
    title: str = Form(),
    description: str = Form(),
    published: bool = Form(False),
    session: AsyncSession = Depends(get_session),
):
    """Обрабатывает форму создания поста."""
    repo = PostRepository(session)
    service = BlogService(repo)

    # Создаём данные для сервиса (PostCreate)
    data = PostCreate(title=title, description=description, published=published)

    try:
        await service.create_post(data)
    except TitleEmptyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except TitleAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return RedirectResponse(url="/admin/", status_code=303)


@auth_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Отдаёт шаблон авторизации."""
    return templates.TemplateResponse(request=request, name="admin/login.html")


@auth_router.post("/login", response_class=HTMLResponse)
async def login_action(request: Request, password: str = Form()):
    """Обрабатывает форму авторизации."""
    if password_hash.verify(password, settings.ADMIN_PASSWORD_HASH):
        token = serializer.dumps({"user": "admin"})
        response = RedirectResponse(url="/admin/", status_code=303)
        response.set_cookie("admin_session", token, httponly=True, max_age=3600)
        return response
    else:
        return templates.TemplateResponse(request=request, name="admin/login.html")


@auth_router.post("/logout")
async def logout():
    """Перенаправляет на главную страницу после выхода из"""
    response = RedirectResponse(url="/page/", status_code=303)
    response.delete_cookie("admin_session")
    return response
