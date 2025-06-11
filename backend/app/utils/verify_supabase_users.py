import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

async def verify_supabase_users():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    conn = await asyncpg.connect(database_url)
    
    try:
        print("Starting Supabase users table verification...\n")

        # verify we can access the auth.users table
        print("1. Verifying auth.users table access...")
        try:
            await conn.fetch("SELECT 1 FROM auth.users LIMIT 1")
            print("✅ Successfully accessed auth.users table")
        except Exception as e:
            print(f"❌ Error accessing auth.users table: {e}")
            return

        # verify required columns exist
        print("\n2. Verifying required columns...")
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'auth'
            AND table_name = 'users'
            AND column_name IN ('id', 'email', 'created_at', 'is_sso_user', 'is_anonymous');
        """)
        
        required_columns = {
            'id': {'type': 'uuid', 'nullable': 'NO'},
            'email': {'type': 'character varying', 'nullable': 'YES'},
            'created_at': {'type': 'timestamp with time zone', 'nullable': 'YES'},
            'is_sso_user': {'type': 'boolean', 'nullable': 'NO'},
            'is_anonymous': {'type': 'boolean', 'nullable': 'NO'}
        }
        
        for col in columns:
            print(f"Checking {col['column_name']}...")
            expected = required_columns[col['column_name']]
            if col['data_type'] == expected['type'] and col['is_nullable'] == expected['nullable']:
                print(f"✅ {col['column_name']} is correct")
            else:
                print(f"❌ {col['column_name']} is incorrect")
                print(f"   Expected: {expected['type']}, {expected['nullable']}")
                print(f"   Got: {col['data_type']}, {col['is_nullable']}")

        # verify indexes
        print("\n3. Verifying indexes...")
        indexes = await conn.fetch("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = 'auth'
            AND tablename = 'users';
        """)
        
        required_indexes = {
            'users_pkey': 'PRIMARY KEY',
            'users_email_key': 'UNIQUE',
            'users_email_partial_key': 'UNIQUE'
        }
        
        for idx in indexes:
            print(f"Checking {idx['indexname']}...")
            if idx['indexname'] in required_indexes:
                print(f"✅ {idx['indexname']} exists")
            else:
                print(f"ℹ️ Additional index: {idx['indexname']}")

        print("\nVerification complete!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(verify_supabase_users()) 