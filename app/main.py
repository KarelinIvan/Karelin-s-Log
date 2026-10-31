from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.controllers import pages, post  # noqa: F401 — регистрирует эндпоинты
from app.controllers.pages import router as pages_router
from app.controllers.router import router as post_router

# Путь к папке с шаблонами (относительно main.py)
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

# Подключение роутеров
app.include_router(post_router)
app.include_router(pages_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
