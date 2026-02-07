#!/usr/bin/env python3
"""
Test script to verify Better Auth endpoints are properly mounted and accessible.
"""

import asyncio
import httpx
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_auth_endpoints():
    """
    Test that all Better Auth endpoints are accessible.
    """
    base_url = "http://localhost:8000"

    # Define the endpoints to test
    endpoints_to_test = [
        # Better Auth compatible endpoints
        ("POST", "/api/auth/sign-up/email"),
        ("POST", "/api/auth/sign-in/email"),
        ("POST", "/api/auth/sign-in/credentials"),
        ("GET", "/api/auth/session"),
        ("POST", "/api/auth/session"),
        ("GET", "/api/auth/user"),
        ("PUT", "/api/auth/user"),
        ("POST", "/api/auth/sign-out"),
        ("POST", "/api/auth/logout"),

        # Standard endpoints
        ("POST", "/api/auth/register"),
        ("POST", "/api/auth/login"),
    ]

    print("Testing Better Auth endpoints...")
    print(f"Base URL: {base_url}")
    print("-" * 60)

    async with httpx.AsyncClient(timeout=10.0) as client:
        for method, endpoint in endpoints_to_test:
            try:
                if method.upper() == "GET":
                    response = await client.get(base_url + endpoint)
                elif method.upper() == "POST":
                    # For POST endpoints, send empty JSON to avoid 422 errors
                    response = await client.post(base_url + endpoint, json={})
                elif method.upper() == "PUT":
                    response = await client.put(base_url + endpoint, json={})

                # Check if we get a reasonable response (should be 401 for auth required, or 422 for validation errors)
                if response.status_code in [200, 401, 400, 422]:
                    status_indicator = "✅" if response.status_code != 401 else "🔐"  # 401 means auth required, which is expected
                    print(f"{status_indicator} {method} {endpoint:<30} -> {response.status_code}")
                else:
                    print(f"❌ {method} {endpoint:<30} -> {response.status_code}")

            except httpx.ConnectError:
                print(f"❌ {method} {endpoint:<30} -> Connection refused (server may not be running)")
            except Exception as e:
                print(f"❌ {method} {endpoint:<30} -> Error: {str(e)}")

    print("-" * 60)
    print("Note: 401 status codes are expected for protected endpoints")
    print("Note: 422 status codes are expected for endpoints requiring proper body data")


def verify_main_app_configuration():
    """
    Verify that main.py has the correct configuration.
    """
    print("\nVerifying main application configuration...")
    print("-" * 60)

    try:
        from src.main import app

        # Check if auth router is included
        auth_routes = []
        for route in app.routes:
            if hasattr(route, 'path') and '/api/auth' in route.path:
                auth_routes.append((route.methods, route.path))

        print(f"✅ Found {len(auth_routes)} authentication routes")

        # Check for specific important routes
        important_routes = [
            '/api/auth/sign-in/email',
            '/api/auth/sign-up/email',
            '/api/auth/session',
            '/api/auth/user',
            '/api/auth/sign-out',
            '/api/auth/login'
        ]

        found_routes = []
        for _, path in auth_routes:
            if path in important_routes:
                found_routes.append(path)

        print(f"✅ Found {len(found_routes)}/{len(important_routes)} important auth routes")

        for route in important_routes:
            status = "✅" if route in [p for _, p in auth_routes] else "❌"
            print(f"  {status} {route}")

        # Check CORS configuration
        cors_found = False
        for middleware in app.user_middleware:
            if hasattr(middleware, 'cls') and 'CORSMiddleware' in str(middleware.cls):
                cors_found = True
                break

        print(f"✅ CORS Middleware: {'✅' if cors_found else '❌'}")

        return True

    except ImportError as e:
        print(f"❌ Could not import main app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error verifying configuration: {e}")
        return False


if __name__ == "__main__":
    print("Better Auth Endpoint Verification Tool")
    print("=" * 60)

    # Verify main app configuration
    config_ok = verify_main_app_configuration()

    # Test endpoints if server is running
    print("\nStarting endpoint connectivity tests...")
    try:
        asyncio.run(test_auth_endpoints())
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nError running endpoint tests: {e}")
        print("This may be because the server is not running.")
        print("To run tests, start the server with: uvicorn src.main:app --reload --port 8000")

    print("\n" + "=" * 60)
    print("Verification complete!")