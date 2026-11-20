from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post

from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel


class PostImage(SQLModel, table=True):
    """
    ORM-модель таблицы 'PostImage' в базе данных PostgreSQL.

    Args:
        id (int): Уникальный идентификатор поста. Является первичным ключом.
            Генерируется автоматически при создании записи.
        post_id (int): Уникальный идентификатор поста. Является вторичным ключом.
        image_data (bytes): Байты изображения.
        order (int): Порядковый номер для сортировки по галереии.
        created_at (datetime): Дата загрузки фотографии.
    """

    __tablename__ = "post_images"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")
    image_data: bytes
    order: int = Field(default=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
        description="Дата загрузки фото",
    )
    post: "Post" = Relationship(back_populates="images")
