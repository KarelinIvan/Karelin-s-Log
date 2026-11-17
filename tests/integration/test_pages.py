from app.models.post import Post


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


async def test_about(async_client):
    """Тест проверяет, отображение страницы 'Обо мне'."""
    response = await async_client.get("/page/about")
    assert response.status_code == 200


async def test_admin_about_post_unautorized(async_client):
    """Тест проверяет, что изменения может внести только авторизованный пользователь."""
    response = await async_client.post("/admin/about", data={"content": "Текст"})
    assert response.status_code == 303


async def test_search_page_returns_results(async_client, search_post):
    """Тест проверяет, что страница поиска отображает найденные посты."""
    response = await async_client.get("/page/search", params={"query": "Python"})
    assert response.status_code == 200
    assert "Изучаем Python для начинающих" in response.text


async def test_search_page_not_results(async_client, search_post):
    """Тест проверяет, что страница поиска отображает заглушку если пост не найден."""
    response = await async_client.get("/page/search", params={"query": "javascript"})
    assert response.status_code == 200
    assert "Изучаем Python для начинающих" not in response.text
    assert "По вашему запросу ничего не найдено..." in response.text


async def test_search_pagination(async_client, test_session):
    """Тест проверяет, что на странице работает пагинация."""

    number = 15
    for post in range(number):
        data = Post(title=f"Пост №{post}", description="Описание", published=True)
        test_session.add(data)

    await test_session.commit()
    response_page_one = await async_client.get("/page/search?query=Пост&page=1")
    assert response_page_one.status_code == 200
    assert "Пост №0" in response_page_one.text
    assert "Пост №10" not in response_page_one.text

    response_page_two = await async_client.get("/page/search?query=Пост&page=2")
    assert response_page_two.status_code == 200
    assert "Пост №10" in response_page_two.text
    assert "Пост №9" not in response_page_two.text


async def test_not_existent_page(async_client):
    """Тест проверяет, что при переходе на несуществующую страницу будет код ошибки 404."""

    response = await async_client.get("/page/not_page")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


async def test_edit_post_not_found(async_client):
    """Тест проверяет, что при попытке отредактировать несуществующий пост будет ошибка 404."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.post(
        "/page/posts/999/edit", data={"title": "Заголовок", "description": "Описание"}
    )
    assert response.status_code == 404


async def test_delete_post_not_found(async_client):
    """Тест проверяет, что при попытке удалить несуществующий пост будет ошибка 404."""
    response_login = await async_client.post(
        "/admin/login", data={"username": "admin", "password": "testpassword"}
    )
    assert response_login.status_code == 303

    response = await async_client.post("/page/posts/999/delete")
    assert response.status_code == 404
