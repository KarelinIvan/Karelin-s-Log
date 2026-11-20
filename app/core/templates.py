import re
from pathlib import Path

import markupsafe
from fastapi.templating import Jinja2Templates

# Путь к папке с шаблонами (относительно main.py)
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def highlight_filter(text: str, query: str) -> markupsafe.Markup:
    """
    Функция для подсветки текста запроса в результатах поиска.

    Args:
        text (str): Текст, в котором нужно найти запрос.
        query (str): Поисковый запрос для подсветки.

    Returns:
        markupsafe.Markup: Возвращает безопасную HTML-строку
            с подсвеченными вхождениями.
    """
    # Экранируем текст и запрос
    safe_text = markupsafe.escape(text)
    safe_query = markupsafe.escape(query)
    pattern = re.escape(safe_query)

    replacement = r"<mark>\g<0></mark>"

    if not safe_query:
        return markupsafe.Markup(safe_text)

    highlighted = re.sub(pattern, replacement, safe_text, flags=re.IGNORECASE)
    return markupsafe.Markup(highlighted)


templates.env.filters["highlight"] = highlight_filter
