from datetime import datetime

from app.schemas.post_base import PostBase


class PostCreate(PostBase):
    """Схема для добавления нового поста в базу данных"""


class PostRead(PostBase):
    """Схема для чтения одного поста из базы данных"""

    id: int
    created_at: datetime
    updated_at: datetime


class PostUpdate(PostBase):
    """Схема для частичного обновления поста."""

    title: str | None = None
    description: str | None = None
    published: bool | None = None

    # Защита от лишних полей
    model_config = {"extra": "forbid"}  # noqa: RUF012
