import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import glob

load_dotenv()

async def run_migrations():
    # connect to database
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    try:
        # get all migration files in order
        migration_files = sorted(glob.glob('app/models/migrations/*.sql'))
        
        # run each migration
        for migration_file in migration_files:
            print(f"Running migration: {migration_file}")
            with open(migration_file, 'r') as f:
                sql = f.read()
                await conn.execute(sql)
            print(f"Completed migration: {migration_file}")
            
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_migrations()) 