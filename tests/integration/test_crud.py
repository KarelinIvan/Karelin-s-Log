from sqlmodel import select

from app.models import Post


async def test_create_post(test_session):
    """
    Тест создает новый пост в таблице posts.
    Проверяет,что посту присвоен ID.
    После создания читает пост из базы данных.
    Проверяет,что все поля заполнены согласно данным post.
    """
    post = Post(title="Тестовый заголовок", description="Тестовое описание")
    test_session.add(post)
    await test_session.commit()
    await test_session.refresh(post)

    # Проверяем, что посту присвоен ID
    assert post.id is not None
    result = await test_session.exec(select(Post).where(Post.id == post.id))
    found = result.one()

    # Проверяем заполнены ли поля
    assert found.title == post.title
    assert found.description == post.description
    assert found.published == post.published


async def test_read_post(test_session, sample_post):
    """
    Тест вызывает фикстуру sample_post для создания поста.
    Далее выполняется проверка чтения поста из базы данных по ID.
    Выполняется проверка данных с исходными.
    """
    result = await test_session.exec(select(Post).where(Post.id == sample_post.id))
    found = result.one()

    # Проверяем, что данные сопадают с исходными
    assert found.title == sample_post.title
    assert found.description == sample_post.description
    assert found.published == sample_post.published


async def test_update_post(test_session, sample_post):
    """
    Тест вызывает фикстуру sample_post для создания поста.
    Меняет содержимое поля title и записывает изменения в базу данных.
    Проверяет что поле title, update_at изменено.

    """
    old_update_at = sample_post.update_at
    sample_post.title = "Новый тестовый заголовок"
    await test_session.commit()
    await test_session.refresh(sample_post)

    # Проверяем что данные изменились
    assert sample_post.title == "Новый тестовый заголовок"
    assert sample_post.update_at > old_update_at
