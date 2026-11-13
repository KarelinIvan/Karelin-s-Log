from sqlmodel import Field, SQLModel


class AboutBase(SQLModel):
    """
    Базовая схема для отображения информации об авторе блога.

    Args:
        content(str): Содержание.
    """

    content: str = Field(
        min_length=100, max_length=10000, description="Содержание страницы 'Обо мне'"
    )
