from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    """
    Базовая схема для всех моделей постов

    Поля:
    title (str): Заголовок поста. Индесируется для быстрого поиска по заголовку
    description (str): Основной текст публикации
    published (bool): Флаг видимости. По умолчанию Fasle, посты не публикуются.
        Это позволяет создавать черновики и планировать их публикацию в ручную.
    """

    title: str = Field(index=True, description="Заголовок поста")
    description: str = Field(description="Содержание")
    published: bool = False
