import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def run_migrations():
    # get database url from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    # connect to database
    conn = await asyncpg.connect(database_url)
    
    try:
        # read and execute migration file
        with open("app/models/migrations/001_create_users_table.sql", "r") as f:
            sql = f.read()
            await conn.execute(sql)
            print("Successfully ran migration: 001_create_users_table.sql")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_migrations()) 