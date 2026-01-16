import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to path

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.tool_call import ToolCall

# This line sets up loggers basically.
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

# Import your models here
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Use the DATABASE_URL from environment variables
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

    # Handle PostgreSQL URL format for asyncpg
    if database_url.startswith("postgresql://"):
        sync_url = database_url.replace("postgresql+asyncpg://", "postgresql://").replace("postgresql://", "postgresql://")
    elif database_url.startswith("postgres://"):
        sync_url = database_url.replace("postgres://", "postgresql://")
    else:
        sync_url = database_url

    connectable = create_engine(sync_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()