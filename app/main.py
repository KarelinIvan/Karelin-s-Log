from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers import pages, post  # noqa: F401 — регистрирует эндпоинты
from app.controllers.pages import router as pages_router
from app.controllers.router import router as post_router
from app.core.templates import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Подключение роутеров
app.include_router(post_router)
app.include_router(pages_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
