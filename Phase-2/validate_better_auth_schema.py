#!/usr/bin/env python3
"""
Validation script to check if the database schema matches Better Auth requirements.
"""

import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def validate_models():
    """Validate that the models have the required Better Auth fields."""
    print("Validating Better Auth compatible models...")

    try:
        from src.models.user import User, UserBase, UserCreate, UserRead

        # Check that UserBase has the required fields
        user_base_annotations = UserBase.__annotations__ if hasattr(UserBase, '__annotations__') else {}

        required_fields = ['email_verified', 'image']
        missing_fields = []

        for field in required_fields:
            if field not in user_base_annotations:
                missing_fields.append(field)

        if missing_fields:
            print(f"[X] Missing fields in UserBase: {missing_fields}")
            return False
        else:
            print("[OK] User model has all required Better Auth fields")

        # Check that User model has all expected fields
        # For SQLModel, fields might be defined differently
        user_attrs = dir(User)
        all_required = ['id', 'email', 'name', 'email_verified', 'image', 'hashed_password', 'created_at', 'updated_at']
        missing_user_fields = []

        for field in all_required:
            if field not in user_attrs:
                missing_user_fields.append(field)

        if missing_user_fields:
            print(f"[X] Missing fields in User model: {missing_user_fields}")
            return False
        else:
            print("[OK] User model structure is correct")

        return True

    except ImportError as e:
        print(f"[X] Error importing User model: {e}")
        return False
    except Exception as e:
        print(f"[X] Error validating User model: {e}")
        return False


def validate_session_account_models():
    """Validate that Session and Account models exist."""
    print("\nValidating Session and Account models...")

    try:
        from src.models.session import Session, SessionCreate, SessionRead
        from src.models.account import Account, AccountCreate, AccountRead

        print("[OK] Session model exists")
        print("[OK] Account model exists")

        # Check basic structure of Session model
        session_attrs = dir(Session)
        required_session_fields = ['id', 'user_id', 'expires_at', 'created_at', 'updated_at']
        missing_session_fields = [f for f in required_session_fields if f not in session_attrs]

        if missing_session_fields:
            print(f"[X] Missing fields in Session model: {missing_session_fields}")
            return False
        else:
            print("[OK] Session model structure is correct")

        # Check basic structure of Account model
        account_attrs = dir(Account)
        required_account_fields = ['id', 'user_id', 'provider_id', 'provider_user_id']
        missing_account_fields = [f for f in required_account_fields if f not in account_attrs]

        if missing_account_fields:
            print(f"[X] Missing fields in Account model: {missing_account_fields}")
            return False
        else:
            print("[OK] Account model structure is correct")

        return True

    except ImportError as e:
        print(f"[X] Error importing Session/Account models: {e}")
        return False
    except Exception as e:
        print(f"[X] Error validating Session/Account models: {e}")
        return False


def validate_auth_api():
    """Validate that auth API has Better Auth compatible endpoints."""
    print("\nValidating auth API endpoints...")

    try:
        from src.api.auth import router

        # Check that the router has the expected routes
        routes = [route.path for route in router.routes]
        expected_routes = ['/get-session', '/logout', '/user']
        missing_routes = [route for route in expected_routes if not any(route in r for r in routes)]

        if missing_routes:
            print(f"[X] Missing Better Auth compatible routes: {missing_routes}")
            return False
        else:
            print("[OK] Auth API has Better Auth compatible endpoints")

        # Check that /register and /login routes still exist
        auth_routes = ['/register', '/login']
        missing_auth = [route for route in auth_routes if not any(route in r for r in routes)]

        if missing_auth:
            print(f"[X] Missing standard auth routes: {missing_auth}")
            return False
        else:
            print("[OK] Standard auth routes still exist")

        return True

    except ImportError as e:
        print(f"[X] Error importing auth API: {e}")
        return False
    except Exception as e:
        print(f"[X] Error validating auth API: {e}")
        return False


def main():
    """Main validation function."""
    print("=" * 60)
    print("Better Auth Schema Validation")
    print("=" * 60)

    all_passed = True

    all_passed &= validate_models()
    all_passed &= validate_session_account_models()
    all_passed &= validate_auth_api()

    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] All validations passed!")
        print("Database schema is ready for Better Auth integration.")
        print("\nNext steps:")
        print("1. Run the migration script to update the database: python migrate_to_better_auth.py")
        print("2. Deploy your backend with the updated schema")
        print("3. Configure Better Auth to use the same database")
    else:
        print("[ERROR] Some validations failed. Please address the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()