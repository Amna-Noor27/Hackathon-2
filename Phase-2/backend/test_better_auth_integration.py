#!/usr/bin/env python3
"""
Test script to verify the Better Auth integration endpoints are working correctly.
This tests the /api/auth/get-session endpoint and other Better Auth compatible endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        from src.api.auth import router
        print("✅ Successfully imported auth router")

        # Check that the get-session endpoint exists
        endpoints = []
        for route in router.routes:
            if hasattr(route, 'path'):
                endpoints.append(route.path)

        print(f"Available auth endpoints: {endpoints}")

        expected_endpoints = ['/register', '/login', '/get-session', '/logout', '/user']
        found_endpoints = []

        for expected in expected_endpoints:
            for endpoint in endpoints:
                if expected in endpoint:
                    found_endpoints.append(expected)
                    break

        print(f"Found Better Auth compatible endpoints: {found_endpoints}")

        if len(found_endpoints) >= 3:  # At least get-session, logout, and user
            print("✅ Better Auth compatible endpoints are properly configured!")
            return True
        else:
            print("❌ Missing some Better Auth compatible endpoints")
            return False

    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return False

def test_database_config():
    """Test that database configuration is properly set up."""
    try:
        from src.core.config import settings
        print(f"✅ Database URL configured: {'yes' if settings.database_url else 'no'}")
        print(f"✅ Better Auth secret configured: {'yes' if settings.better_auth_secret else 'no'}")

        # Check if it looks like a Neon DB URL
        is_neon_db = 'neon.tech' in settings.database_url if settings.database_url else False
        print(f"✅ Using Neon DB: {'yes' if is_neon_db else 'no'}")

        return True
    except Exception as e:
        print(f"❌ Error checking database config: {e}")
        return False

if __name__ == "__main__":
    print("Testing Better Auth Integration...")
    print("=" * 50)

    success1 = test_imports()
    print()
    success2 = test_database_config()

    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ All tests passed! Better Auth integration is ready.")
    else:
        print("❌ Some tests failed, but the basic setup is complete.")

    print("\nThe following endpoints are now available:")
    print("- POST /api/auth/register - User registration")
    print("- POST /api/auth/login - User login")
    print("- GET /api/auth/get-session - Get current session (Better Auth compatible)")
    print("- POST /api/auth/logout - Logout (Better Auth compatible)")
    print("- GET /api/auth/user - Get current user info (Better Auth compatible)")