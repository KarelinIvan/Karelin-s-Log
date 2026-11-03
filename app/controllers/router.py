from fastapi import APIRouter, Depends

from app.controllers.dependencies import log_request, verify_admin

# API-роутер
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(log_request)],
)

# HTML-роутер
pages_router = APIRouter(
    prefix="/page", tags=["pages"], dependencies=[Depends(log_request)]
)

# Admin-роутер
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin), Depends(log_request)],
)
