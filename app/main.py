from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import post  # noqa: F401 — регистрирует эндпоинты
from app.controllers.router import router as post_router
from app.database.session import create_db_and_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(db_engine=engine)
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

# Подключение роутеров
app.include_router(post_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
