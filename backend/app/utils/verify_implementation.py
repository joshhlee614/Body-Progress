import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

async def verify_implementation():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    conn = await asyncpg.connect(database_url)
    
    try:
        print("Starting comprehensive verification...\n")

        # 1. Verify table structure
        print("1. Verifying table structure...")
        table_info = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        print("Table structure:")
        for col in table_info:
            print(f"- {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']}, default: {col['column_default']})")
        print()

        # 2. Verify index
        print("2. Verifying index...")
        index_info = await conn.fetch("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'users';
        """)
        print("Indexes:")
        for idx in index_info:
            print(f"- {idx['indexname']}: {idx['indexdef']}")
        print()

        # 3. Test data operations
        print("3. Testing data operations...")
        
        # Test insert
        test_email = "test@example.com"
        user = await conn.fetchrow(
            """
            INSERT INTO users (email)
            VALUES ($1)
            RETURNING id, email, created_at
            """,
            test_email
        )
        print(f"Insert test: Successfully inserted user with email {user['email']}")
        
        # Test duplicate email constraint
        try:
            await conn.execute(
                "INSERT INTO users (email) VALUES ($1)",
                test_email
            )
            print("❌ Error: Duplicate email was allowed!")
        except asyncpg.UniqueViolationError:
            print("✅ Duplicate email constraint working correctly")
        
        # Test null email constraint
        try:
            await conn.execute("INSERT INTO users (email) VALUES (NULL)")
            print("❌ Error: NULL email was allowed!")
        except asyncpg.NotNullViolationError:
            print("✅ NULL email constraint working correctly")
        
        # Test created_at default
        new_user = await conn.fetchrow(
            "SELECT created_at FROM users WHERE email = $1",
            test_email
        )
        if new_user['created_at'].tzinfo == timezone.utc:
            print("✅ created_at timestamp has timezone information")
        else:
            print("❌ Error: created_at timestamp missing timezone information")
        
        # Test UUID generation
        if user['id'].version == 4:
            print("✅ UUID is being generated correctly")
        else:
            print("❌ Error: UUID is not being generated correctly")
        
        # Clean up
        await conn.execute("DELETE FROM users WHERE email = $1", test_email)
        print("\nCleaned up test data")
        
        print("\nVerification complete!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(verify_implementation()) 