from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Глобальные настройки приложения.
    Чтение происходит из файла .env в папке проекта.
    """

    # Полный адрес подключения
    # (драйвер/диалект, учётные данные, хост и порт, имя базы данных)
    DATABASE_URL: str

    # Настройки FastAPI
    DEBUG_SQLALCHEMY: bool
    APP_PORT: int

    # Хеш
    ADMIN_PASSWORD_HASH: str

    # Секретный ключ приложения
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()  # type: ignore
