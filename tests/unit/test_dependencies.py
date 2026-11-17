from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from itsdangerous import SignatureExpired

from app.controllers.dependencies import verify_admin


async def test_verify_admin_expired_cookie():
    """
    Юнит-тест: проверяет, что при истёкшей куке
    verify_admin выбрасывает HTTPException с кодом 401.
    """
    fake_request = MagicMock()

    fake_request.cookies.get.return_value = "any_token"

    with (
        patch(
            "app.controllers.dependencies.serializer.loads",
            side_effect=SignatureExpired("expired"),
        ),
        pytest.raises(HTTPException) as exc_info,
    ):
        await verify_admin(fake_request)

    assert exc_info.value.status_code == 401
