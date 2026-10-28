from fastapi import Request


async def log_request(request: Request):
    """Логирует метод и путь входящего запроса."""
    print(f"{request.method} {request.url.path}")
