"""
Database module initialization and exports.

This module exports core database components for use throughout the application:
- Base: SQLAlchemy declarative base for ORM models
- engine: Database connection engine
- AsyncSessionLocal: Factory for creating async database sessions
- get_db: Dependency function for obtaining database sessions
- init_db: Function to initialize database tables
- drop_db: Function to drop all database tables
- close_db: Function to close database connections
"""

from app.db.core import Base, engine, AsyncSessionLocal
from app.db.session import get_db, close_db
from app.db.migrations import init_db, drop_db

__all__ = [
    "Base",
    "engine",
    "AsyncSessionLocal",
    "get_db",
    "init_db",
    "drop_db",
    "close_db",
]
