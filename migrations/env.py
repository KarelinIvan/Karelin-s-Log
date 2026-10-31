import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

# Импортируем модели
import app.models  # noqa: F401

# Импортируем настройки
from app.core.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем Alembic, откуда брать модели для генерации
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций в 'offline' режиме
    (генерация SQL без подключения к базе данных.)
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Синхронная функция для запуска миграций внутри асинхронного проекта."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Асинхронный запуск миграций."""
    # Создаём асинхронный движок, используя URL из настроек
    connectable = create_async_engine(settings.DATABASE_URL)

    async with connectable.connect() as connection:
        # run_sync используется для моста между async и sync API Alembic
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (с подключением к БД)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
