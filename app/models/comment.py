from datetime import UTC, datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import AutoString, Field, Relationship

from app.schemas.comment_base import CommentBase


class Comment(CommentBase, table=True):
    """
    ORM-модель таблицы «Comment» в базе данных PostgreSQL.

    Args:
        id (int): Уникальный идентификатор комментария. Является первичным ключом.
            Генерируется автоматически при создании записи.
        post_id (int): Уникальный идентификатор поста. Является вторичным ключом.
        author_name (str): Имя автора комментария.
        text (str): Содержание комментария.
        created_at (datetime): Дата создания комментария.
                    Заполняется текущим временем UTC при добавлении новой записи как
                    на уровне приложения (`default_factory`), так и на уровне
                    базы данных (`server_default`).
        email (EmailStr): Email автора комментария.
        parent_id (int | None): Ссылка на родительский комментарий.
    """

    __tablename__ = "comments"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
        description="Дата создания",
    )
    email: EmailStr = Field(sa_type=AutoString, description="Email автора")
    parent_id: int | None = Field(default=None, foreign_key="comments.id")
    parent: Optional["Comment"] = Relationship(
        back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"}
    )
    replies: list["Comment"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"},
    )
