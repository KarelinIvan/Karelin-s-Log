async def test_create_post(async_client, test_session):
    """Тест проверяет успешное создание поста через api."""
    response = await async_client.post(
        "/posts/",
        json={
            "title": "Тестовый пост",
            "description": "Описание",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовый пост"
    assert "id" in data


async def test_create_post_empty_title(async_client, test_session):
    """
    Тест проверяет падение ошибки 400 при создании нового поста
    с пустым значением title, через api.
    """
    response = await async_client.post(
        "/posts/",
        json={
            "title": "",
            "description": "Описание",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Title не может быть пустым"


async def test_create_post_title_already_exists(async_client, sample_post):
    """
    Тест проверяет падение ошибки 409 при создании нового поста
    со значением title, уже существующем в базе данных, через api.
    """
    response = await async_client.post(
        "/posts/",
        json={
            "title": sample_post.title,
            "description": "Описание",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Пост с таким title уже существует"
