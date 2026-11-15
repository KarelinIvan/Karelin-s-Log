from sqlmodel import select

from app.database.repositories.post import PostRepository
from app.models.post import Post
from app.schemas.post import PostCreate


async def test_repository_create(test_session):
    """
    Тест создает новый пост в базе данных.
    Проверяет, что посту присвоено ID.
    Проверяет, что все поля заполнены верно.
    """
    post_repo = PostRepository(test_session)
    data = PostCreate(
        title="Тестовый заголовок",
        description="Описание",
    )
    post = await post_repo.create(data)

    # Проверяем присвоение id
    assert post.id is not None

    # Проверяем данные
    result = await test_session.exec(select(Post).where(Post.id == post.id))
    found = result.one()
    assert found.title == data.title
    assert found.description == data.description
    assert found.published is False


async def test_repository_get_by_id(test_session, sample_post):
    """Тест проверяет поиск постов по ID в репозитории."""
    post_repo = PostRepository(test_session)

    # Ищем существующий пост (из фикстуры)
    found = await post_repo.get_by_id(sample_post.id)

    # Проверяем, что пост найден и совпадает по ID
    assert found is not None
    assert found.id == sample_post.id

    # Проверяем, что несуществующий ID возвращает None
    missing_post = await post_repo.get_by_id(9999)
    assert missing_post is None


async def test_search_full_title_post(test_session, search_post):
    """Тест проверяет поиск по полному совпадению заголовка."""
    post_repo = PostRepository(test_session)

    search = await post_repo.search("Изучаем Python для начинающих")
    assert len(search) >= 1
    assert search[0].title == search_post.title


async def test_search_title_start_post(test_session, search_post):
    """Тест проверяет, что поиск находит пост по совпадению первого слова в заголовке."""
    post_repo = PostRepository(test_session)

    search = await post_repo.search("Изучаем")
    assert len(search) >= 1
    assert search[0].title == search_post.title


async def test_search_title_contains(test_session, search_post):
    """Тест проверяет поиск по слову в середине заголовка."""
    post_repo = PostRepository(test_session)

    search = await post_repo.search("Python")
    assert len(search) >= 1
    assert search[0].title == search_post.title


async def test_search_description(test_session, search_post):
    """Тест проверяет поиск по описанию."""
    post_repo = PostRepository(test_session)

    search = await post_repo.search("программирования")
    assert len(search) >= 1
    assert search[0].description == search_post.description


async def test_search_not_found(test_session, search_post):
    """Тест проверяет, что нет совпадений ни в заголовке, ни в описании."""
    post_repo = PostRepository(test_session)

    search = await post_repo.search("java")
    assert len(search) == 0


async def test_count_search_returns_corrent_count(test_session, search_post):
    """Тест проверяет, что метод count_search правильно считает количество найденных постов."""
    post_repo = PostRepository(test_session)

    count = await post_repo.count_search("Python")
    assert count == 1


async def test_count_search_returns_zero(test_session, search_post):
    """
    Тест проверяет, что метод count_search возращает ноль,
    если постов с нужным запросом не найдено.
    """
    post_repo = PostRepository(test_session)

    count = await post_repo.count_search("Java")
    assert count == 0
