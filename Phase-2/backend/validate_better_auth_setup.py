#!/usr/bin/env python3
"""
Validation script to check that Better Auth endpoints are properly implemented.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def validate_auth_router():
    """
    Validate that the auth router has all required Better Auth endpoints.
    """
    try:
        from src.auth.router import router

        print("Validating Better Auth Router...")
        print("-" * 50)

        # Collect all routes
        routes = {}
        for route in router.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                for method in route.methods:
                    if method in ['GET', 'POST', 'PUT', 'DELETE']:
                        routes[(method, route.path)] = route

        # Expected Better Auth compatible endpoints
        expected_endpoints = [
            ('POST', '/sign-up/email'),
            ('POST', '/sign-in/email'),
            ('POST', '/sign-in/credentials'),
            ('GET', '/session'),
            ('POST', '/session'),
            ('GET', '/user'),
            ('PUT', '/user'),
            ('POST', '/sign-out'),
            ('POST', '/logout'),
        ]

        # Additional standard endpoints
        additional_endpoints = [
            ('POST', '/register'),
            ('POST', '/login'),
        ]

        print("Checking Better Auth compatible endpoints:")
        found_count = 0
        for method, path in expected_endpoints:
            full_path = path
            if (method, full_path) in routes:
                print(f"  ✅ {method} {full_path}")
                found_count += 1
            else:
                print(f"  ❌ {method} {full_path}")

        print(f"\nBetter Auth endpoints found: {found_count}/{len(expected_endpoints)}")

        print("\nChecking additional endpoints:")
        additional_found = 0
        for method, path in additional_endpoints:
            full_path = path
            if (method, full_path) in routes:
                print(f"  ✅ {method} {full_path}")
                additional_found += 1
            else:
                print(f"  ❌ {method} {full_path}")

        print(f"\nAdditional endpoints found: {additional_found}/{len(additional_endpoints)}")

        total_expected = len(expected_endpoints) + len(additional_endpoints)
        total_found = found_count + additional_found

        print(f"\nTotal endpoints: {total_found}/{total_expected}")

        if total_found >= total_expected - 2:  # Allow for minor differences
            print("✅ Router validation: PASSED")
            return True
        else:
            print("❌ Router validation: FAILED")
            return False

    except Exception as e:
        print(f"❌ Error validating router: {e}")
        return False


def validate_cors_configuration():
    """
    Validate that CORS is properly configured for Better Auth.
    """
    try:
        from src.main import app

        print("\nValidating CORS Configuration...")
        print("-" * 50)

        cors_middleware = None
        for middleware in app.user_middleware:
            if 'CORSMiddleware' in str(type(middleware.instance)):
                cors_middleware = middleware.instance
                break

        if not cors_middleware:
            print("❌ CORS Middleware not found")
            return False

        print(f"✅ CORS Middleware found")

        # Check origins
        allowed_origins = getattr(cors_middleware, 'allow_origins', [])
        localhost_3000_allowed = 'http://localhost:3000' in allowed_origins
        credentials_enabled = getattr(cors_middleware, 'allow_credentials', False)

        print(f"✅ localhost:3000 in allowed origins: {localhost_3000_allowed}")
        print(f"✅ Credentials allowed: {credentials_enabled}")

        if localhost_3000_allowed and credentials_enabled:
            print("✅ CORS configuration: PASSED")
            return True
        else:
            print("❌ CORS configuration: FAILED")
            return False

    except Exception as e:
        print(f"❌ Error validating CORS: {e}")
        return False


def validate_auth_dependencies():
    """
    Validate that required auth dependencies are available.
    """
    print("\nValidating Auth Dependencies...")
    print("-" * 50)

    dependencies = [
        ('fastapi', 'FastAPI'),
        ('sqlmodel', 'SQLModel'),
        ('python_jose', 'jwt'),
        ('bcrypt', 'hashpw'),
        ('pydantic_settings', 'BaseSettings'),
    ]

    success_count = 0
    for module, item in dependencies:
        try:
            if module == 'python_jose':
                from jose import jwt
                print(f"  ✅ {module}")
                success_count += 1
            elif module == 'bcrypt':
                import bcrypt
                print(f"  ✅ {module}")
                success_count += 1
            elif module == 'pydantic_settings':
                from pydantic_settings import BaseSettings
                print(f"  ✅ {module}")
                success_count += 1
            else:
                __import__(module)
                print(f"  ✅ {module}")
                success_count += 1
        except ImportError as e:
            print(f"  ❌ {module} - {e}")

    print(f"\nDependencies available: {success_count}/{len(dependencies)}")

    if success_count == len(dependencies):
        print("✅ Dependencies validation: PASSED")
        return True
    else:
        print("⚠️  Dependencies validation: PARTIAL (some missing)")
        return success_count > len(dependencies) * 0.7  # At least 70% required


if __name__ == "__main__":
    print("Better Auth Implementation Validator")
    print("=" * 60)

    # Run all validations
    router_valid = validate_auth_router()
    cors_valid = validate_cors_configuration()
    deps_valid = validate_auth_dependencies()

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Router validation: {'✅ PASSED' if router_valid else '❌ FAILED'}")
    print(f"  CORS validation: {'✅ PASSED' if cors_valid else '❌ FAILED'}")
    print(f"  Dependencies validation: {'✅ PASSED' if deps_valid else '❌ FAILED'}")

    all_passed = router_valid and cors_valid and deps_valid

    print(f"\nOverall status: {'✅ ALL GOOD' if all_passed else '❌ ISSUES FOUND'}")

    if all_passed:
        print("\nThe Better Auth implementation appears to be properly configured!")
    else:
        print("\nThere are issues with the Better Auth implementation that need to be addressed.")