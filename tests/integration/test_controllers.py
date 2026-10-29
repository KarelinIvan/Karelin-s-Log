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


async def test_get_post(async_client, sample_post):
    """Тест проверяет успешное получение поста по ID, через api."""
    response = await async_client.get(f"/posts/{sample_post.id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == sample_post.id
    assert data["title"] == sample_post.title


async def test_get_not_found(async_client):
    """Тест проверяет ошибку PostNotFoundError, если такого поста нет."""
    msg_id = 9999
    response = await async_client.get(f"posts/{msg_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Пост с id: {msg_id} не найден"
