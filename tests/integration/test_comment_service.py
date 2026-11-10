from app.database.repositories.comment import CommentRepository
from app.schemas.comment import CommentCreate
from app.services.comment_service import CommentService


async def test_comment_service_create(test_session, sample_post):
    """Тест проверяет, работу сервиса при создании комментариев."""
    comment_repo = CommentRepository(test_session)
    comment_service = CommentService(comment_repo)
    data_comment = CommentCreate(
        author_name="Иван", text="Комментарий", email="ivan@example.ru"
    )
    comment = await comment_service.create_comment(data_comment, sample_post.id)

    assert comment is not None
    assert comment.author_name == data_comment.author_name
    assert comment.text == data_comment.text
    assert comment.email == data_comment.email
    assert comment.post_id == sample_post.id


async def test_comment_service_get_comments(test_session, sample_post):
    """Тест проверяет, работу сервиса при создании комментариев (сначал старые)."""
    comment_repo = CommentRepository(test_session)
    comment_service = CommentService(comment_repo)
    data_comment_one = CommentCreate(
        author_name="Иван", text="Первый комментарий", email="ivan@example.ru"
    )
    data_comment_two = CommentCreate(
        author_name="Иван", text="Второй комментарий", email="ivan@example.ru"
    )
    await comment_service.create_comment(data_comment_one, sample_post.id)
    await comment_service.create_comment(data_comment_two, sample_post.id)

    comments = await comment_service.get_comments(sample_post.id)

    assert len(comments) == 2
    assert comments[0].text == "Первый комментарий"
    assert comments[1].text == "Второй комментарий"
