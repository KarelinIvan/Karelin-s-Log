from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class CommentBase(SQLModel):
    """
    Базовая схема для всех моделей комментариев.

    Args:
        author_name (str): Автор комментария.
        text (str): Текст комментария.
        email (EmailStr): Email автора.
    """

    author_name: str = Field(description="Автор")
    text: str = Field(description="Содержание")
    email: EmailStr = Field(description="Email автора")
