import nh3

ALLOWED_TAGS = {
    "p",
    "br",
    "strong",
    "em",
    "u",
    "s",
    "a",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "blockquote",
    "code",
    "pre",
    "span",
}

ALLOWED_ATTRIBUTES = {"a": {"href", "title"}}


def sanitize_html(html: str | None) -> str:
    """
    Функция для очистки HTML-содержимого постов, перед записью в базу данных.
    Удаляет опасные теги и атрибуты для защиты от XSS-атак.

    Args:
        html (str | None): Принимает неочищенную HTML-строку или None.

    Returns:
        str: Очищенная HTML-строка. Если на входе был None, вернётся пустая строка.
    """

    if not html:
        return ""
    return nh3.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
