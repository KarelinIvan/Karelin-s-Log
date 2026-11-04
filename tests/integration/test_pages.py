async def test_index_page(async_client):
    """Тест проверяет, что корректно открывается главная страница."""
    response = await async_client.get("/page/")
    assert response.status_code == 200


async def test_post_detail_page(async_client, sample_post):
    """Тест проверяет, что корректно открывается страница с детальной информацией поста."""
    response = await async_client.get(f"/page/posts/{sample_post.id}")
    assert response.status_code == 200


async def test_edit_post_page(async_client, sample_post):
    """Тест проверяет, что страница редактирования открывается и содержит данные поста."""
    response = await async_client.get(f"/page/posts/{sample_post.id}/edit")
    assert response.status_code == 200
    assert sample_post.title in response.text


async def test_admin_dashboard(async_client):
    """Тест проверяет, что корректно открывается страница панели администратора."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.get("/admin/")
    assert response.status_code == 200


async def test_admin_create_post_page(async_client):
    """Тест проверяет, что корректно открывается страница для создания поста в админ панели."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.get("/admin/posts/create")
    assert response.status_code == 200


async def test_admin_create_post_action(async_client, test_session):
    """Тестп роверяет, что форма для создания поста корректно работает."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.post(
        "/admin/posts/create",
        data={"title": "Заголовок", "description": "Описание", "published": True},
    )
    assert response.status_code == 303
