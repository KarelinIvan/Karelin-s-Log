from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.about import About


class AboutRepository:
    def __init__(self, session: AsyncSession):
        """Сохраняет сессию."""
        self.session = session

    async def get(self) -> About | None:
        """
        Возвращает запись обо мне.

        Returns:
            About: ORM-объект с присвоенным id и заполненым updated_at.
        """
        result = await self.session.exec(select(About))
        return result.first()

    async def update(self, about: About, data: dict) -> About:
        """
        Метод обновляет данные на странице 'Обо мне'.

        Args:
            about(About): ORM-объект записи.
            data(dict): Словарь с данными для обновления.
        Returns:
            About: Обновлённая запись.
        """
        # список разрешенных ключей
        allowed_fields = ["content", "photo"]

        for key, value in data.items():
            if key in allowed_fields:
                setattr(about, key, value)

        self.session.add(about)
        await self.session.commit()
        await self.session.refresh(about)
        return about
