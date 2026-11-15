from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.controllers import admin, pages, post  # noqa: F401 — регистрирует эндпоинты
from app.controllers.router import admin_router, auth_router, pages_router
from app.controllers.router import router as post_router
from app.core.templates import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Перенаправляет с корня проекта на главную страницу блога."""
    return RedirectResponse(url="/page/")


@app.exception_handler(HTTPException)
async def redirect_auth_page(request: Request, exc: HTTPException):
    """
    Перенаправляет на страницу авторизации,если сессия истекла.
    Иначе возвращает json ответ ошибки, с кодом ошибки.
    """
    if exc.status_code == 401:
        return RedirectResponse(url="/admin/login", status_code=303)
    else:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Подключение роутеров
app.include_router(post_router)
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
