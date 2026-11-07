from app.database.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate


async def test_comment_repository_create(test_session, sample_post):
    """Тест проверяет, создание комментария к посту."""
    comment_repo = CommentRepository(test_session)
    data_comment = CommentCreate(
        author_name="Иван", text="Комментарий", email="ivan@example.ru"
    )
    comment = await comment_repo.create(data_comment, sample_post.id)

    assert comment.id is not None
    assert comment.author_name == data_comment.author_name
    assert comment.text == data_comment.text
    assert comment.email == data_comment.email
    assert comment.post_id == sample_post.id


async def test_comment_repository_get_by_post_id(test_session, sample_post):
    """Тест проверяет, сортировку комментариев по дате создания (сначала старые)."""
    comment_repo = CommentRepository(test_session)
    data_comment_one = CommentCreate(
        author_name="Иван", text="Первый комментарий", email="ivan@example.ru"
    )
    data_comment_two = CommentCreate(
        author_name="Иван", text="Второй комментарий", email="ivan@example.ru"
    )

    await comment_repo.create(data_comment_one, sample_post.id)
    await comment_repo.create(data_comment_two, sample_post.id)

    comments = await comment_repo.get_by_post_id(sample_post.id)

    assert len(comments) == 2
    assert comments[0].text == "Первый комментарий"
    assert comments[1].text == "Второй комментарий"
