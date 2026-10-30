class TitleEmptyError(Exception):
    """Title не может быть пустым."""


class TitleAlreadyExistsError(Exception):
    """Пост с таким title уже существует."""


class PostNotFoundError(Exception):
    """Пост с таким id не найден."""
