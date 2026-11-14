from app.database.repositories.about import AboutRepository
from app.models.about import About


class AboutService:
    def __init__(self, repo: AboutRepository):
        self.repo = repo

    async def get(self) -> About | None:
        """
        Возвращает запись страницы 'Обо мне'.

        Returns:
            About | None: ORM-объект записи или None.
        """
        return await self.repo.get()

    async def update(self, about: About, data: dict) -> About:
        """
        Обновляет данные на странице 'Обо мне'.

        Args:
            about(About): Существующие ORM-объект записи.
            data(dict): Словарь с полями для изменения (content, photo).

        Returns:
            About: Обновлённый ORM-объект.
        """
        return await self.repo.update(about, data)
