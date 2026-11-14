from app.database.repositories.about import AboutRepository
from app.models.about import About


async def test_about_repository_get_empty(test_session):
    """Тест проверяет, что репозиторий пустой."""
    about_repo = AboutRepository(test_session)

    about = await about_repo.get()

    assert about is None


async def test_about_repository_create(test_session):
    """Тест проверяет, что данные записываются."""
    about_repo = AboutRepository(test_session)

    data = About(content="Тестовый текст" * 20)
    test_session.add(data)
    await test_session.commit()
    await test_session.refresh(data)

    about = await about_repo.get()
    assert about is not None
    assert about.content == "Тестовый текст" * 20


async def test_about_repository_update(test_session):
    """Тест проверяет, что репозиторий обновляется данными."""
    about_repo = AboutRepository(test_session)

    data = About(content="Текст" * 30)
    test_session.add(data)
    await test_session.commit()
    await test_session.refresh(data)

    about = await about_repo.update(data, {"content": "Тестовый текст" * 20})
    assert about.content == "Тестовый текст" * 20
