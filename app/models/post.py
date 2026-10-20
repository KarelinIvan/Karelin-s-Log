from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import func
from sqlmodel import Field

from app.schemas.post_base import PostBase


class Post(PostBase, table=True):
    """
    ORM-модель таблицы «Post» в базе данных PostgreSQL.

    Args:
        id (int):  Уникальный идентификатор поста. Является первичным ключом.
            Генерируется автоматически при создании записи.
        created_at (datetime): Дата создания поста.
            Заполняется текущим временем UTC при добавлении новой записи как
            на уровне приложения (`default_factory`), так и на уровне
            базы данных (`server_default`).
        update_at (datetime): Дата последнего изменения поста.
            Обновляется каждый раз при изменении записи. На уровне БД это
            происходит автоматически благодаря параметру
            `onupdate="CURRENT_TIMESTAMP"`. Это поле также имеет клиентский
            дефолт для корректной работы ORM.
    """

    # явно задаем название таблицы в бд
    __tablename__ = "posts"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
        description="Дата создания",
    )
    update_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
        nullable=False,
        sa_column_kwargs={
            "onupdate": func.now(),
        },
        description="Дата изменения",
    )
