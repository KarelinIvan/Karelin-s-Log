from fastapi import APIRouter, Depends

from app.controllers.dependencies import log_request

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(log_request)],
)
