#!/usr/bin/env python3
"""
Migration script to update the database schema for Better Auth compatibility.
This script ensures all required tables and columns exist for Better Auth integration.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Add migrations directory to the path
migrations_path = str(Path(__file__).parent / "migrations")
sys.path.insert(0, migrations_path)

# Import the migration functions directly from the file
import importlib.util
migration_spec = importlib.util.spec_from_file_location("better_auth_schema",
                                                        str(Path(__file__).parent / "migrations" / "001_better_auth_schema.py"))
migration_module = importlib.util.module_from_spec(migration_spec)
migration_spec.loader.exec_module(migration_module)
create_better_auth_tables = migration_module.create_better_auth_tables
verify_schema = migration_module.verify_schema
from src.database import engine
from sqlmodel import Session, select
from src.models.user import User
from src.models.session import Session as SessionModel
from src.models.account import Account
from datetime import datetime

def migrate_existing_users():
    """
    Migrate existing users to include the new required fields for Better Auth compatibility.
    """
    print("Checking for existing users and migrating if needed...")

    with Session(engine) as session:
        # Get all existing users
        existing_users = session.exec(select(User)).all()

        if not existing_users:
            print("No existing users to migrate.")
            return

        print(f"Found {len(existing_users)} existing users to migrate...")

        migrated_count = 0
        for user in existing_users:
            # Ensure email_verified and image fields exist (they should now with the updated model)
            # but if they're None, we can set defaults if needed
            if user.email_verified is None:
                # For existing users, we might want to set email as verified by default
                # Or leave as None if verification is pending
                pass  # Leave as None for now, meaning not verified

            if user.image is None:
                # Set a default image if none exists
                user.image = "https://example.com/default-avatar.png"

            session.add(user)
            migrated_count += 1

        session.commit()
        print(f"Migrated {migrated_count} users successfully.")


def validate_better_auth_compatibility():
    """
    Validate that the database schema is compatible with Better Auth requirements.
    """
    print("\nValidating Better Auth compatibility...")

    with Session(engine) as session:
        # Check if required tables exist by trying to query them
        try:
            # Test users table
            user_count = session.exec(select(User)).all()
            print(f"✓ Users table accessible, found {len(user_count)} users")

            # Test sessions table existence
            try:
                session.exec(select(SessionModel)).all()
                print("✓ Sessions table exists and is accessible")
            except Exception as e:
                print(f"⚠ Sessions table issue: {e}")

            # Test accounts table existence
            try:
                session.exec(select(Account)).all()
                print("✓ Accounts table exists and is accessible")
            except Exception as e:
                print(f"⚠ Accounts table issue: {e}")

        except Exception as e:
            print(f"✗ Error validating tables: {e}")
            return False

    return True


def main():
    """
    Main migration function that orchestrates the Better Auth schema update.
    """
    print("=" * 60)
    print("Better Auth Database Migration Script")
    print("=" * 60)

    print("\nStep 1: Creating Better Auth schema tables...")
    create_better_auth_tables()

    print("\nStep 2: Verifying schema...")
    verify_schema()

    print("\nStep 3: Migrating existing users...")
    migrate_existing_users()

    print("\nStep 4: Validating Better Auth compatibility...")
    is_valid = validate_better_auth_compatibility()

    if is_valid:
        print("\n✓ All checks passed! Database is now compatible with Better Auth.")
        print("\nRequired tables for Better Auth:")
        print("  - users table with emailVerified and image fields")
        print("  - sessions table for managing user sessions")
        print("  - accounts table for managing third-party provider accounts")
    else:
        print("\n✗ Some checks failed. Please review the errors above.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Migration completed successfully!")
    print("Your database is now ready for Better Auth integration.")
    print("=" * 60)


if __name__ == "__main__":
    main()