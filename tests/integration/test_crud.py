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

    # Проверяем, что посту присвое ID
    assert post.id is not None
    result = await test_session.exec(select(Post).where(Post.id == post.id))
    found = result.one()

    # Проверяем заполнены ли поля
    assert found.title == post.title
    assert found.description == post.description
    assert found.published == post.published
