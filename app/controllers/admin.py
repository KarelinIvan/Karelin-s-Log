from fastapi import Request
from fastapi.responses import HTMLResponse

from app.controllers.router import admin_router as router
from app.core.templates import templates


@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    """Тестовая страница админки."""
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={"message": "Админка работает!"},
    )
