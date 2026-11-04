from fastapi import HTTPException, Request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pwdlib import PasswordHash

from app.core.settings import settings

password_hash = PasswordHash.recommended()

serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="admin-session")


async def log_request(request: Request):
    """Логирует метод и путь входящего запроса."""
    print(f"{request.method} {request.url.path}")


async def verify_admin(request: Request):
    """Проверяет сессию администратора."""

    token = request.cookies.get("admin_session")
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        data = serializer.loads(token, max_age=3600)
    except SignatureExpired:  # Сначала ловим истёкший срок
        raise HTTPException(status_code=401, detail="Session expired")
    except BadSignature:  # Потом ловим неверную подпись
        raise HTTPException(status_code=401, detail="Invalid session token")

    return data.get("user")
