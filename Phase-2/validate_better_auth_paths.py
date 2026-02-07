"""
Script to validate Better Auth paths and ensure they match between frontend and backend
"""
import requests
import sys
from typing import Dict, List

def validate_auth_paths(base_url: str) -> Dict[str, bool]:
    """
    Validate that the expected Better Auth paths are available on the backend
    """
    # Expected Better Auth paths
    expected_paths = [
        "/api/auth/sign-up/email",           # Sign up with email
        "/api/auth/sign-in/email",          # Sign in with email
        "/api/auth/session",                # Get session (GET and POST)
        "/api/auth/user",                   # Get user info
        "/api/auth/sign-out",               # Sign out
    ]

    # Legacy paths for compatibility
    legacy_paths = [
        "/api/auth/sign-up/email-password", # Legacy sign up
        "/api/auth/sign-in/credentials",    # Legacy sign in
        "/api/auth/logout",                 # Legacy logout
        "/api/auth/get-session",            # Legacy get session
    ]

    results = {}

    for path in expected_paths + legacy_paths:
        try:
            # Test with GET request (some endpoints may accept GET)
            response = requests.get(f"{base_url}{path}", timeout=5)
            results[path] = response.status_code != 404
            print(f"✓ {path}: {response.status_code}" if results[path] else f"✗ {path}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            results[path] = False
            print(f"✗ {path}: Error - {str(e)}")

    return results

def check_cors_configuration(base_url: str) -> bool:
    """
    Check if CORS is properly configured for cross-origin requests
    """
    try:
        # Send OPTIONS request to check CORS preflight
        response = requests.options(
            f"{base_url}/api/auth/session",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            },
            timeout=5
        )

        cors_headers = response.headers
        has_credentials = cors_headers.get('Access-Control-Allow-Credentials', '').lower() == 'true'
        has_origin = 'http://localhost:3000' in cors_headers.get('Access-Control-Allow-Origin', '')

        print(f"CORS Allow-Credentials: {cors_headers.get('Access-Control-Allow-Credentials', 'Not set')}")
        print(f"CORS Allow-Origin: {cors_headers.get('Access-Control-Allow-Origin', 'Not set')}")

        return has_credentials and has_origin
    except Exception as e:
        print(f"CORS check failed: {str(e)}")
        return False

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

    print(f"Validating Better Auth paths for {base_url}")
    print("=" * 50)

    # Validate auth paths
    results = validate_auth_paths(base_url)

    print("\nCORS Configuration Check:")
    print("-" * 25)
    cors_ok = check_cors_configuration(base_url)

    print("\nSummary:")
    print("-" * 10)
    total_paths = len(results)
    successful_paths = sum(1 for v in results.values() if v)

    print(f"Paths working: {successful_paths}/{total_paths}")
    print(f"CORS properly configured: {'Yes' if cors_ok else 'No'}")

    if successful_paths == total_paths and cors_ok:
        print("\n✅ All authentication paths are properly configured!")
        sys.exit(0)
    else:
        print("\n❌ Some authentication paths are not working or CORS is misconfigured.")
        sys.exit(1)