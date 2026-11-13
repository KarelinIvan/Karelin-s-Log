from datetime import UTC, datetime

from sqlalchemy import func
from sqlmodel import Field

from app.schemas.about_base import AboutBase


class About(AboutBase, table=True):
    """
    ORM-модель таблицы «About» в базе данных PostgreSQL.

    Args:
        id(int) Уникальный идентификатор.
        updated_at(datetime) Дата обновления.
    """

    __tablename__ = "about"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"server_default": func.now()},
    )
