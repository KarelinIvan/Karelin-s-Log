from sqlmodel import select

from app.database.repositories.post import PostRepository
from app.models.post import Post
from app.schemas.post import PostCreate


async def test_admin_posts_list(async_client, test_session):
    """Тест проверяет, что корректно открывается страница админки со списком постов."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.get("/admin/posts")
    assert response.status_code == 200


async def test_admin_posts_filter(async_client, test_session):
    """
    Тест проверяет работу фильтра админки.
    Отображение постов со статусом 'Опубликовано'.
    Отображение постов со статусом 'Черновик'.
    Отображение всех постов.
    """

    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    post_repo = PostRepository(test_session)
    data_draft = PostCreate(title="Заголовок черновика", description="Описание")
    data_publish = PostCreate(
        title="Опубликованный заголовок", description="Описание", published=True
    )
    await post_repo.create(data_draft)
    await post_repo.create(data_publish)

    response_draft = await async_client.get("/admin/posts?status=draft")
    assert "Опубликованный заголовок" not in response_draft.text
    assert "Заголовок черновика" in response_draft.text

    response_publish = await async_client.get("/admin/posts?status=published")
    assert "Опубликованный заголовок" in response_publish.text
    assert "Заголовок черновика" not in response_publish.text

    response_all = await async_client.get("/admin/posts?status=all")
    assert "Опубликованный заголовок" in response_all.text
    assert "Заголовок черновика" in response_all.text


async def test_admin_action_publish(async_client, test_session):
    """Тест проверяет действие в админке, публикация поста."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    post_repo = PostRepository(test_session)
    data_draft = PostCreate(title="Заголовок", description="Описание")
    post = await post_repo.create(data_draft)

    response_publish = await async_client.post(
        f"/admin/posts/{post.id}/action", data={"action": "publish"}
    )
    assert response_publish.status_code == 303

    await test_session.refresh(post)
    updated_post = await post_repo.get_by_id(post.id)
    assert updated_post is not None
    assert updated_post.published is True


async def test_admin_action_unpublish(async_client, test_session):
    """Тест проверяет действие в админке, снятие поста с публикации."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    post_repo = PostRepository(test_session)
    data_publish = PostCreate(title="Заголовок", description="Описание", published=True)
    post = await post_repo.create(data_publish)

    response_publishe = await async_client.post(
        f"/admin/posts/{post.id}/action", data={"action": "unpublish"}
    )
    assert response_publishe.status_code == 303

    await test_session.refresh(post)
    updated_post = await post_repo.get_by_id(post.id)
    assert updated_post is not None
    assert updated_post.published is False


async def test_admin_action_delete(async_client, test_session):
    """Тест проверяет действие в админке, удаление поста."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    post_repo = PostRepository(test_session)
    data_delete = PostCreate(title="Заголовок", description="Описание")
    post = await post_repo.create(data_delete)

    response_delete = await async_client.post(
        f"/admin/posts/{post.id}/action", data={"action": "delete"}
    )
    assert response_delete.status_code == 303

    delete_post = await post_repo.get_by_id(post.id)
    assert delete_post is None


async def test_verify_admin_invalid_cookie(async_client):
    """
    Тест проверяет, что при невалидной куке пользователя
    перенаправляет на страницы авторизации.
    """
    async_client.cookies.set("admin_session", "invalid_token")
    response = await async_client.get("/admin/about")
    assert response.status_code == 303


async def test_create_post_empty_title(async_client, test_session):
    """Тест проверяет, что при создании поста с пустым заголовком пользователь получит ошибку 400."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.post(
        "/admin/posts/create", data={"title": " ", "description": "Описание"}
    )
    assert response.status_code == 400


async def test_create_post_title_exists(async_client, test_session):
    """Тест проверяет, что при создании поста с занятым заголовком пользователь получит ошибку 409."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    post_repo = PostRepository(test_session)
    data = PostCreate(title="Заголовок занят", description="Описание")
    await post_repo.create(data)

    response = await async_client.post(
        "/admin/posts/create",
        data={"title": "Заголовок занят", "description": "Описание"},
    )
    assert response.status_code == 409


async def test_admin_create_post_with_files(async_client, test_session):
    """Тест проверяет, что при создании поста обложка загружается корректно."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    # Тестовые байты обложки (минимальный PNG 1x1)
    cover_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"

    response = await async_client.post(
        "/admin/posts/create",
        data={
            "title": "Заголовок",
            "description": "Описание",
            "content": "<p>Содержание</p>",
        },
        files={"cover_image": ("image.png", cover_data, "image/png")},
    )
    assert response.status_code == 303

    result = await test_session.exec(select(Post).where(Post.title == "Заголовок"))
    found = result.one()

    assert found is not None
    assert found.cover_image is not None
    assert found.cover_image == cover_data
