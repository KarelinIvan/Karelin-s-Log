import secrets

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pwdlib import PasswordHash

from app.core.settings import settings

password_hash = PasswordHash.recommended()


async def log_request(request: Request):
    """Логирует метод и путь входящего запроса."""
    print(f"{request.method} {request.url.path}")


async def verify_admin(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    """
    Проверяет логин и пароль администратора.

    Returns:
        str: Имя пользователя (при успешной проверке).

    Raises:
        HTTPException: 401, если логин или пароль неверны.
    """

    username = secrets.compare_digest(credentials.username, "admin")
    password = password_hash.verify(credentials.password, settings.ADMIN_PASSWORD_HASH)

    if username and password:
        return credentials.username
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
