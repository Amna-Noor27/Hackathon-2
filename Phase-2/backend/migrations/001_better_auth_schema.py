"""
Database migration script to align the schema with Better Auth requirements.
This script creates or updates the user, session, and account tables to match Better Auth specifications.
"""
import asyncio
from sqlmodel import Session, create_engine, select
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def create_better_auth_tables():
    """
    Create or update tables to match Better Auth schema requirements.
    """
    with engine.connect() as conn:
        # Check if we're using PostgreSQL (Neon)
        is_postgresql = 'postgresql' in DATABASE_URL.lower()

        if is_postgresql:
            print("Detected PostgreSQL/Neon database")

            # Create or update users table with Better Auth schema
            conn.execute(text("""
                -- Create users table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    email_verified TIMESTAMP WITH TIME ZONE,
                    image TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
            """))

            # Create sessions table with Better Auth schema
            conn.execute(text("""
                -- Create sessions table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS sessions (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
            """))

            # Create accounts table with Better Auth schema
            conn.execute(text("""
                -- Create accounts table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS accounts (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    provider_id VARCHAR(255) NOT NULL,
                    provider_user_id VARCHAR(255) NOT NULL,
                    access_token TEXT,
                    refresh_token TEXT,
                    id_token TEXT,
                    token_type VARCHAR(255),
                    scope TEXT,
                    expires_at BIGINT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(provider_id, provider_user_id)
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
                CREATE INDEX IF NOT EXISTS idx_accounts_provider ON accounts(provider_id, provider_user_id);
            """))

            # Check if the existing user table needs to be updated
            # First, check what columns exist in the current users table
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
            """)).fetchall()

            columns = {row[0]: {'type': row[1], 'nullable': row[2]} for row in result}

            # Add missing columns to users table if needed
            if 'email_verified' not in columns:
                print("Adding email_verified column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN email_verified TIMESTAMP WITH TIME ZONE;"))

            if 'image' not in columns:
                print("Adding image column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN image TEXT;"))

            # Check if the old user table (from SQLModel) exists and migrate data if needed
            old_table_exists = conn.execute(text("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables
                   WHERE table_name = 'user'
                );
            """)).scalar()

            if old_table_exists:
                print("Found old 'user' table, migrating data if needed...")

                # Check if users table is empty and old user table has data
                users_count = conn.execute(text("SELECT COUNT(*) FROM users;")).scalar()
                old_users_count = conn.execute(text("SELECT COUNT(*) FROM user;")).scalar()

                if users_count == 0 and old_users_count > 0:
                    print("Migrating data from old 'user' table to new 'users' table...")

                    # Copy data from old table to new table
                    conn.execute(text("""
                        INSERT INTO users (id, name, email, created_at, updated_at)
                        SELECT id, name, email, created_at, updated_at
                        FROM user
                        WHERE id NOT IN (SELECT id FROM users);
                    """))

                    print(f"Migrated {conn.execute(text('SELECT COUNT(*) FROM users;')).scalar()} users")

        else:
            # Handle SQLite case (for local development)
            print("Detected SQLite database")

            # Create or update users table with Better Auth schema
            conn.execute(text("""
                -- Create users table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT UNIQUE NOT NULL,
                    email_verified TIMESTAMP,
                    image TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            """))

            # Create sessions table with Better Auth schema
            conn.execute(text("""
                -- Create sessions table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
            """))

            # Create accounts table with Better Auth schema
            conn.execute(text("""
                -- Create accounts table with Better Auth schema if it doesn't exist
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    provider_id TEXT NOT NULL,
                    provider_user_id TEXT NOT NULL,
                    access_token TEXT,
                    refresh_token TEXT,
                    id_token TEXT,
                    token_type TEXT,
                    scope TEXT,
                    expires_at INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(provider_id, provider_user_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
                CREATE INDEX IF NOT EXISTS idx_accounts_provider ON accounts(provider_id, provider_user_id);
            """))

            # Check if the existing user table needs to be updated
            result = conn.execute(text("""
                PRAGMA table_info(users);
            """)).fetchall()

            columns = [row[1] for row in result]  # Column names are in the second position

            if 'email_verified' not in columns:
                print("Adding email_verified column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN email_verified TIMESTAMP;"))

            if 'image' not in columns:
                print("Adding image column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN image TEXT;"))

        conn.commit()
        print("Better Auth schema tables created/updated successfully!")


def verify_schema():
    """
    Verify that the schema matches Better Auth requirements.
    """
    with engine.connect() as conn:
        is_postgresql = 'postgresql' in DATABASE_URL.lower()

        if is_postgresql:
            # Check users table
            users_columns = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
            """)).fetchall()

            print("\nUsers table structure:")
            for col in users_columns:
                print(f"  {col[0]}: {col[1]}, nullable: {col[2]}")

            # Check sessions table
            sessions_columns = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'sessions'
                ORDER BY ordinal_position;
            """)).fetchall()

            print("\nSessions table structure:")
            for col in sessions_columns:
                print(f"  {col[0]}: {col[1]}, nullable: {col[2]}")

            # Check accounts table
            accounts_columns = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'accounts'
                ORDER BY ordinal_position;
            """)).fetchall()

            print("\nAccounts table structure:")
            for col in accounts_columns:
                print(f"  {col[0]}: {col[1]}, nullable: {col[2]}")

        else:
            # Check users table for SQLite
            users_columns = conn.execute(text("PRAGMA table_info(users);")).fetchall()

            print("\nUsers table structure:")
            for col in users_columns:
                print(f"  {col[1]}: {col[2]}, nullable: {not col[3]}")

            # Check sessions table for SQLite
            sessions_columns = conn.execute(text("PRAGMA table_info(sessions);")).fetchall()

            print("\nSessions table structure:")
            for col in sessions_columns:
                print(f"  {col[1]}: {col[2]}, nullable: {not col[3]}")

            # Check accounts table for SQLite
            accounts_columns = conn.execute(text("PRAGMA table_info(accounts);")).fetchall()

            print("\nAccounts table structure:")
            for col in accounts_columns:
                print(f"  {col[1]}: {col[2]}, nullable: {not col[3]}")


if __name__ == "__main__":
    print("Starting Better Auth schema migration...")
    print(f"Database URL: {DATABASE_URL.replace('@', '***@')[:50]}..." if '@' in DATABASE_URL else f"Database URL: {DATABASE_URL}")

    create_better_auth_tables()
    verify_schema()

    print("\nMigration completed successfully!")
    print("The database now has the required tables for Better Auth integration:")
    print("- users table with emailVerified and image fields")
    print("- sessions table for managing user sessions")
    print("- accounts table for managing third-party provider accounts")