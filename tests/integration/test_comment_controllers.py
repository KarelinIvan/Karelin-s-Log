async def test_post_comment_action(async_client, sample_post):
    """Тест проверяет работу формы комментариев."""
    comment = await async_client.post(
        f"/page/posts/{sample_post.id}/comments",
        data={
            "author_name": "Иван",
            "text": "Hello World!",
            "email": "ivan@example.ru",
        },
    )
    assert comment.status_code == 303

    response = await async_client.get(f"/page/posts/{sample_post.id}")
    assert "Hello World!" in response.text
