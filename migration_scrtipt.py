import asyncio
from db_module import DataBase
from database.migration.db_migration import migration_db

async def run_migrations():
    db = DataBase()
    await migration_db(db)

if __name__ == '__main__':
    asyncio.run(run_migrations())
