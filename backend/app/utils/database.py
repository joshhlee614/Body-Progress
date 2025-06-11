from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# convert postgresql:// to postgresql+asyncpg:// for async support
DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgresql://", "postgresql+asyncpg://")

# create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# dependency to get db session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 