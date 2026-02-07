"""
Database initialization script for creating tables in Neon Serverless PostgreSQL.
This script will create the User, Task, Session, and Account tables based on the SQLModel metadata.
These tables are required for Better Auth compatibility.
"""
import asyncio
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
from src.models.session import Session
from src.models.account import Account
from src.core.config import settings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables or use default
DATABASE_URL = os.getenv("DATABASE_URL", settings.database_url)

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    # For PostgreSQL (Neon)
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)


def create_tables():
    """Create all tables defined in the SQLModel metadata."""
    print("Connecting to database...")
    print(f"Database URL: {DATABASE_URL.replace('@', '***@')[:50]}..." if '@' in DATABASE_URL else f"Database URL: {DATABASE_URL}")

    try:
        # Create all tables from SQLModel metadata
        print("Creating tables...")
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully!")

        # List the tables that were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nTables in database: {tables}")

        expected_tables = ['user', 'task', 'session', 'account']
        for table in expected_tables:
            if table in tables:
                print(f"✓ {table.capitalize()} table created")
            else:
                print(f"? {table.capitalize()} table not found")

    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def main():
    """Main function to run the database initialization."""
    print("=== Database Initialization Script ===")
    print("This script will create the required tables for Better Auth compatibility in your Neon database.\n")

    create_tables()

    print("\n=== Database Initialization Complete ===")
    print("Your User, Task, Session, and Account tables should now appear in the Neon console!")


if __name__ == "__main__":
    main()