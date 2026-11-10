from sqlmodel import select

from app.database.repositories.comment import CommentRepository
from app.models.comment import Comment
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


async def test_comment_root_return_with_replies(test_session, sample_post):
    """
    Тест проверяет, что метод get_by_post_id возвращает только корневые
    комментарии, а ответы на них вкладываются в атрибут replies.
    """
    comment_repo = CommentRepository(test_session)
    data_comment_root = CommentCreate(
        author_name="Иван", text="Комментарий", email="ivan@example.py"
    )
    root_comment = await comment_repo.create(data_comment_root, sample_post.id)

    data_comment_replies = CommentCreate(
        author_name="Админ", text="Ответ", email="admin@example.ru"
    )
    await comment_repo.create(
        data_comment_replies, sample_post.id, parent_id=root_comment.id
    )

    await test_session.refresh(root_comment)
    comments = await comment_repo.get_by_post_id(sample_post.id)
    assert len(comments) == 1
    assert len(comments[0].replies) == 1
    assert comments[0].replies[0].text == data_comment_replies.text


async def test_comment_cascade_delete(test_session, sample_post):
    """
    Тест проверяет, что при удалении корневого комментария его ответы удаляются
    автоматически (каскадное удаление на уровне базы данных).
    """
    comment_repo = CommentRepository(test_session)
    data_comment_root = CommentCreate(
        author_name="Иван", text="Комментарий", email="ivan@example.ru"
    )
    comment_root = await comment_repo.create(data_comment_root, sample_post.id)

    data_comment_replies = CommentCreate(
        author_name="Админ", text="Ответ", email="admin@example.ru"
    )
    await comment_repo.create(
        data_comment_replies, sample_post.id, parent_id=comment_root.id
    )

    await test_session.delete(comment_root)
    await test_session.commit()

    comments = await test_session.exec(select(Comment))
    assert len(comments.all()) == 0
