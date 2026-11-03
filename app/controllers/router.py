from fastapi import APIRouter, Depends

from app.controllers.dependencies import log_request, verify_admin

# API-роутер
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(log_request)],
)

# HTML-роутер
pages_router = APIRouter(prefix="/page", tags=["pages"])

# Admin-роутер
admin_router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(verify_admin)]
)
