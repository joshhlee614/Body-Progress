import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_users_table():
    # get database url from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    # connect to database
    conn = await asyncpg.connect(database_url)
    
    try:
        # test inserting a user
        test_email = "test@example.com"
        user = await conn.fetchrow(
            """
            INSERT INTO users (email)
            VALUES ($1)
            RETURNING id, email, created_at
            """,
            test_email
        )
        print("Successfully inserted test user:", dict(user))

        # verify the user exists
        users = await conn.fetch("SELECT * FROM users")
        print("\nAll users in database:")
        for user in users:
            print(dict(user))

        # clean up test data
        await conn.execute("DELETE FROM users WHERE email = $1", test_email)
        print("\nCleaned up test data")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(test_users_table()) 