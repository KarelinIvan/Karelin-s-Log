from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.session import create_db_and_tables, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(db_engine=engine)
    print("База данных готова")
    yield
    print("Выключение")


app = FastAPI()


@app.get("/home")
async def get_home():
    return {"message": "Сервер работает"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
