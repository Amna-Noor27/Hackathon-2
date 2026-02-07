"""
Migration script to ensure the tasks table has a user_id column that references
Better Auth's users table.

Note: Since Better Auth manages the users table externally, we cannot create
a traditional foreign key constraint. Instead, we ensure the user_id column
exists with proper data type and constraints to match Better Auth's user_id format.
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


def check_and_fix_user_id_column():
    """
    Check if the tasks table has a user_id column with proper constraints.
    If missing, add the column.
    """
    with engine.connect() as conn:
        # Check if user_id column exists in tasks table
        if 'postgresql' in DATABASE_URL:
            # For PostgreSQL
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'task' AND column_name = 'user_id'
            """)).fetchone()
        elif 'sqlite' in DATABASE_URL:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(task)")).fetchall()
            result = next((row for row in result if row[1] == 'user_id'), None)
        else:
            print(f"Unsupported database type for URL: {DATABASE_URL}")
            return

        if result is None:
            print("user_id column not found in tasks table. Adding it...")

            # Add user_id column to tasks table
            if 'postgresql' in DATABASE_URL:
                alter_query = text("""
                    ALTER TABLE task ADD COLUMN user_id VARCHAR(255) NOT NULL;

                    -- Create index on user_id for better performance
                    CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);
                """)
            else:  # SQLite
                # For SQLite, we need to recreate the table with the new column
                alter_query = text("""
                    -- Create new table with user_id column
                    CREATE TABLE task_new (
                        id TEXT NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        completed BOOLEAN NOT NULL,
                        user_id TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL,
                        PRIMARY KEY (id)
                    );

                    -- Copy data from old table to new table (assuming all belong to a default user for now)
                    INSERT INTO task_new (id, title, description, completed, user_id, created_at, updated_at)
                    SELECT id, title, description, completed, 'default_user_id_placeholder', created_at, updated_at
                    FROM task;

                    -- Drop old table and rename new table
                    DROP TABLE task;
                    ALTER TABLE task_new RENAME TO task;

                    -- Create index
                    CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);
                """)

            conn.execute(alter_query)
            conn.commit()
            print("user_id column added successfully!")
        else:
            print(f"user_id column already exists: {result}")

            # Check if there's an index on user_id for performance
            if 'postgresql' in DATABASE_URL:
                index_result = conn.execute(text("""
                    SELECT indexname
                    FROM pg_indexes
                    WHERE tablename = 'task' AND indexname = 'idx_task_user_id'
                """)).fetchone()
            else:  # SQLite
                index_result = conn.execute(text("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'index' AND name = 'idx_task_user_id'
                """)).fetchone()

            if not index_result:
                print("Creating index on user_id column...")
                index_query = text("CREATE INDEX idx_task_user_id ON task(user_id);")
                conn.execute(index_query)
                conn.commit()
                print("Index created successfully!")


if __name__ == "__main__":
    print("Starting database schema verification and migration...")
    check_and_fix_user_id_column()
    print("Migration completed successfully!")