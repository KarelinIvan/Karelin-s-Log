from fastapi import FastAPI

app = FastAPI()


@app.get("/home")
async def get_home():
    return {"message": "Сервер работает"}
