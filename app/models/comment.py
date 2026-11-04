from datetime import UTC, datetime

from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import AutoString, Field, SQLModel


class Comment(SQLModel, table=True):
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
    """

    __tablename__ = "comments"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id")
    author_name: str = Field(description="Автор")
    text: str = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
        description="Дата создания",
    )
    email: EmailStr = Field(sa_type=AutoString, description="Email автора")
