"""
Database configuration and setup for Fantasy F1 application.

This module provides:
- Async SQLAlchemy engine configuration
- Async session factory
- Base class for ORM models
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy async engine configuration
# Uses SQLite with aiosqlite driver for async support
# In production, consider using PostgreSQL with asyncpg
engine = create_async_engine(
    "sqlite+aiosqlite:///./fantasy_f1.db",
    echo=False,  # Set to True for SQL query logging
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    
    Yields:
        AsyncSession: An async database session
        
    Usage in FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    Should be called once on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """
    Drop all tables from the database.
    
    Warning: This is destructive and should only be used in development/testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_db() -> None:
    """
    Close the database engine and connection pool.
    
    Should be called on application shutdown.
    """
    await engine.dispose()
