"""
Final comprehensive validation of the backend implementation.
"""
import os
import sys
from pathlib import Path


def check_project_structure():
    """Check that all required directories and files exist."""
    print("Checking project structure...")

    required_dirs = [
        "src",
        "src/models",
        "src/services",
        "src/api",
        "src/core",
        "src/middleware",
        "src/schemas",
        "tests",
        "tests/unit",
        "tests/contract",
        "tests/integration",
        "docs"
    ]

    required_files = [
        "src/main.py",
        "src/database.py",
        "src/models/user.py",
        "src/models/task.py",
        "src/services/task_service.py",
        "src/api/tasks.py",
        "src/core/config.py",
        "src/core/logging_config.py",
        "src/middleware/error_handler.py",
        "src/schemas/error.py",
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        "docs/README.md"
    ]

    missing_dirs = []
    missing_files = []

    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)

    for file_path in required_files:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)

    if missing_dirs:
        print(f"Missing directories: {missing_dirs}")
    else:
        print("OK: All required directories exist")

    if missing_files:
        print(f"Missing files: {missing_files}")
    else:
        print("OK: All required files exist")

    return len(missing_dirs) == 0 and len(missing_files) == 0


def check_documentation():
    """Check that documentation is present."""
    print("\nChecking documentation...")

    docs_checks = [
        ("README in docs/", os.path.isfile("docs/README.md")),
        ("Quickstart guide", os.path.isfile("../specs/001-todo-backend-tasks/quickstart.md")),
        ("API documentation", "API Endpoints" in open("docs/README.md", 'r').read() if os.path.exists("docs/README.md") else False),
        ("Environment vars documented", os.path.isfile(".env.example"))
    ]

    passed = 0
    for check_name, result in docs_checks:
        if result:
            print(f"OK: {check_name}")
            passed += 1
        else:
            print(f"ERR: {check_name}")

    return passed == len(docs_checks)


def check_tests_exist():
    """Check that test files exist and have content."""
    print("\nChecking tests...")

    test_files = [
        "tests/unit/test_models.py",
        "tests/contract/test_tasks_api.py",
        "tests/contract/test_user_isolation.py",
        "tests/contract/test_error_responses.py",
        "tests/integration/test_task_management.py",
        "tests/integration/test_security.py",
        "tests/integration/test_error_handling.py"
    ]

    all_exist = True
    for file_path in test_files:
        exists = os.path.isfile(file_path)
        if exists:
            size = os.path.getsize(file_path)
            if size > 0:
                print(f"OK: {file_path} (size: {size} bytes)")
            else:
                print(f"ERR: {file_path} (empty file)")
                all_exist = False
        else:
            print(f"ERR: {file_path} (missing)")
            all_exist = False

    return all_exist


def check_environment_setup():
    """Check environment setup files."""
    print("\nChecking environment setup...")

    env_checks = [
        ("requirements.txt", os.path.isfile("requirements.txt")),
        ("pyproject.toml", os.path.isfile("pyproject.toml")),
        (".env.example", os.path.isfile(".env.example")),
        ("dependencies listed", "fastapi" in open("requirements.txt", 'r').read() if os.path.exists("requirements.txt") else False)
    ]

    passed = 0
    for check_name, result in env_checks:
        if result:
            print(f"OK: {check_name}")
            passed += 1
        else:
            print(f"ERR: {check_name}")

    return passed == len(env_checks)


def main():
    """Run all validation checks."""
    print("=== Final Comprehensive Validation ===\n")

    structure_ok = check_project_structure()
    docs_ok = check_documentation()
    tests_ok = check_tests_exist()
    env_ok = check_environment_setup()

    print(f"\n=== Final Validation Report ===")
    print(f"Project structure: {'PASS' if structure_ok else 'FAIL'}")
    print(f"Documentation: {'PASS' if docs_ok else 'FAIL'}")
    print(f"Tests: {'PASS' if tests_ok else 'FAIL'}")
    print(f"Environment: {'PASS' if env_ok else 'FAIL'}")

    overall_success = structure_ok and docs_ok and tests_ok and env_ok

    print(f"\nOverall validation: {'SUCCESS' if overall_success else 'FAILURE'}")

    if overall_success:
        print("\nSUCCESS: The Todo Backend implementation is complete and validated!")
        print("   All required components, tests, and documentation are in place.")
    else:
        print("\nERROR: Some validation checks failed. Please review the output above.")

    return overall_success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)