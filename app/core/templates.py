from pathlib import Path

from fastapi.templating import Jinja2Templates

# Путь к папке с шаблонами (относительно main.py)
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
