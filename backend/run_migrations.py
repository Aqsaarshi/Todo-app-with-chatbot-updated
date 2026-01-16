import asyncio
from alembic.config import Config
from alembic import command

def run_migration():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()