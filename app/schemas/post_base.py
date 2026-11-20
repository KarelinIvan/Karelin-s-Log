from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    """
    Базовая схема для всех моделей постов

    Поля:
    title (str): Заголовок поста. Индексируется для быстрого поиска по заголовку
    description (str): Основной текст публикации
    published (bool): Флаг видимости. По умолчанию False, посты не публикуются.
        Это позволяет создавать черновики и планировать их публикацию вручную.
    content (str | None): HTML-содержание поста. Может быть None, если пост не содержит HTML.
    video_url (str | None): Ссылка на видео. Может быть None, если пост не содержит видео.
    """

    title: str = Field(index=True, description="Заголовок поста")
    description: str = Field(description="Содержание")
    published: bool = False
    content: str | None = Field(default=None, description="HTML-содержание поста")
    video_url: str | None = Field(default=None, description="Ссылка на видео")
