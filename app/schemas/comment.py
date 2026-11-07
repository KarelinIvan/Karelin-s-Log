from datetime import datetime

from app.schemas.comment_base import CommentBase


class CommentCreate(CommentBase):
    """Схема для добавления нового комментария в базу данных."""

    parent_id: int | None = None


class CommentRead(CommentBase):
    """Схема для чтения одного комментария из базы данных."""

    id: int
    post_id: int
    created_at: datetime
    parent_id: int | None = None
