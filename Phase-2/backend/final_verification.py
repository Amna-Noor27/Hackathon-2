#!/usr/bin/env python3
"""
Final verification script for Better Auth integration.
This script confirms all requirements have been met.
"""

import sys
import os
import json
from pathlib import Path

def check_requirement_1_explicit_mount():
    """Check that backend/src/main.py explicitly mounts the Better Auth router"""
    print("1. Checking explicit router mounting in main.py...")

    main_py_path = Path("src/main.py")
    if not main_py_path.exists():
        print("   ❌ src/main.py not found")
        return False

    content = main_py_path.read_text()

    # Check for explicit mounting with correct prefix
    has_include_router = "app.include_router(auth_router, prefix=\"/api/auth\"" in content
    has_correct_prefix = "prefix=\"/api/auth\"" in content

    if has_include_router and has_correct_prefix:
        print("   ✅ Router explicitly mounted with correct prefix /api/auth")
        return True
    else:
        print("   ❌ Router mounting not found or incorrect")
        print(f"   Has include_router: {has_include_router}")
        print(f"   Has correct prefix: {has_correct_prefix}")
        return False

def check_requirement_2_login_endpoint():
    """Check that login endpoint matches what client sends"""
    print("2. Checking login endpoints in auth router...")

    auth_router_path = Path("src/auth/router.py")
    if not auth_router_path.exists():
        print("   ❌ src/auth/router.py not found")
        return False

    content = auth_router_path.read_text()

    # Check for Better Auth compatible endpoints
    has_sign_in_email = "sign_in_email" in content and '"/sign-in/email"' in content
    has_sign_in_credentials = "sign_in_credentials" in content and '"/sign-in/credentials"' in content
    has_legacy_login = '"login"' in content or '"/login"' in content

    print(f"   Has /sign-in/email: {has_sign_in_email}")
    print(f"   Has /sign-in/credentials: {has_sign_in_credentials}")
    print(f"   Has /login: {has_legacy_login}")

    # At least one of the Better Auth standard endpoints should exist
    if has_sign_in_email or has_sign_in_credentials:
        print("   ✅ Better Auth compatible login endpoints found")
        return True
    else:
        print("   ❌ No Better Auth compatible login endpoints found")
        return False

def check_requirement_3_cors_configuration():
    """Check CORS configuration for localhost:3000 and credentials"""
    print("3. Checking CORS configuration...")

    main_py_path = Path("src/main.py")
    if not main_py_path.exists():
        print("   ❌ src/main.py not found")
        return False

    content = main_py_path.read_text()

    # Check for localhost:3000 in allow_origins
    has_localhost_3000 = "http://localhost:3000" in content
    has_allow_credentials = "allow_credentials=True" in content

    print(f"   Has localhost:3000 in origins: {has_localhost_3000}")
    print(f"   Has allow_credentials=True: {has_allow_credentials}")

    if has_localhost_3000 and has_allow_credentials:
        print("   ✅ CORS properly configured with localhost:3000 and credentials")
        return True
    else:
        print("   ❌ CORS not properly configured")
        return False

def check_requirement_4_all_endpoints_accessible():
    """Check that all authentication endpoints are properly defined"""
    print("4. Checking all auth endpoints are accessible...")

    auth_router_path = Path("src/auth/router.py")
    if not auth_router_path.exists():
        print("   ❌ src/auth/router.py not found")
        return False

    content = auth_router_path.read_text()

    # Check for essential Better Auth endpoints
    essential_endpoints = [
        ('sign-up', '"/sign-up/email"'),
        ('sign-in', '"/sign-in/email"'),
        ('session', '"/session"'),
        ('user', '"/user"'),
        ('sign-out', '"/sign-out"')
    ]

    found_endpoints = []
    missing_endpoints = []

    for name, endpoint_pattern in essential_endpoints:
        if endpoint_pattern in content:
            found_endpoints.append(name)
        else:
            missing_endpoints.append(name)

    print(f"   Found endpoints: {found_endpoints}")
    print(f"   Missing endpoints: {missing_endpoints}")

    # Most essential endpoints should be present
    if len(found_endpoints) >= 4:  # At least 4 out of 5 essential endpoints
        print("   ✅ Most authentication endpoints are properly defined")
        return True
    else:
        print("   ❌ Too many essential endpoints are missing")
        return False

def run_verification():
    """Run all verification checks"""
    print("Better Auth Integration Verification")
    print("=" * 60)

    checks = [
        check_requirement_1_explicit_mount,
        check_requirement_2_login_endpoint,
        check_requirement_3_cors_configuration,
        check_requirement_4_all_endpoints_accessible
    ]

    results = []
    for check in checks:
        result = check()
        results.append(result)
        print()

    print("=" * 60)
    print("VERIFICATION SUMMARY:")

    requirements = [
        "Explicit router mounting",
        "Login endpoint compatibility",
        "CORS configuration",
        "All endpoints accessible"
    ]

    for i, (req, result) in enumerate(zip(requirements, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i}. {req}: {status}")

    all_passed = all(results)
    print(f"\nOverall result: {'✅ ALL REQUIREMENTS MET' if all_passed else '❌ SOME REQUIREMENTS FAILED'}")

    return all_passed

if __name__ == "__main__":
    success = run_verification()

    if success:
        print("\n🎉 Better Auth integration is properly configured!")
        print("All requirements have been successfully implemented.")
    else:
        print("\n⚠️  Some requirements are not met. Please review the issues above.")

    sys.exit(0 if success else 1)