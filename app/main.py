from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI()


@app.get("/home")
async def get_home():
    return {"message": "Сервер работает"}
