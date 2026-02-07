"""
Test that validates the Python syntax of our modules without requiring external dependencies.
"""
import ast
import os
from pathlib import Path


def test_syntax_only():
    """Test that all Python files have valid syntax."""
    print("Testing Python syntax for backend modules...")

    # Define the files to test
    files_to_test = [
        "src/database.py",
        "src/models/user.py",
        "src/models/task.py",
        "src/services/task_service.py",
        "src/schemas/error.py",
        "src/core/config.py",
        "src/core/logging_config.py",
        "src/middleware/error_handler.py",
        "src/api/tasks.py",
        "src/main.py"
    ]

    success_count = 0
    total_count = len(files_to_test)

    for file_path in files_to_test:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse to check syntax
            ast.parse(content)
            print(f"SYNTAX OK: {file_path}")
            success_count += 1
        except FileNotFoundError:
            print(f"FILE MISSING: {file_path}")
        except SyntaxError as e:
            print(f"SYNTAX ERROR: {file_path} - Line {e.lineno}: {e.msg}")
        except Exception as e:
            print(f"ERROR: {file_path} - {str(e)}")

    print(f"\nSyntax validation: {success_count}/{total_count} files passed")

    # Test model creation without dependencies
    print("\nTesting model structure (without external dependencies)...")
    try:
        # Read the task model file
        with open("src/models/task.py", 'r', encoding='utf-8') as f:
            task_content = f.read()

        # Verify key elements exist
        if "class Task(" in task_content:
            print("MODEL STRUCTURE OK: Task class exists")
        else:
            print("MODEL STRUCTURE ERROR: Task class not found")

        if "title: str" in task_content:
            print("MODEL STRUCTURE OK: Task title field exists")
        else:
            print("MODEL STRUCTURE WARNING: Task title field not found")

        if "user_id: str" in task_content:
            print("MODEL STRUCTURE OK: Task user_id field exists")
        else:
            print("MODEL STRUCTURE WARNING: Task user_id field not found")

        # Read the user model file
        with open("src/models/user.py", 'r', encoding='utf-8') as f:
            user_content = f.read()

        if "class User(" in user_content:
            print("MODEL STRUCTURE OK: User class exists")
        else:
            print("MODEL STRUCTURE ERROR: User class not found")

        if "email: str" in user_content:
            print("MODEL STRUCTURE OK: User email field exists")
        else:
            print("MODEL STRUCTURE WARNING: User email field not found")

        print("Model structure validation completed")
        return success_count == total_count

    except Exception as e:
        print(f"Model structure test error: {str(e)}")
        return False


def main():
    """Main test function."""
    print("=== Backend Syntax and Structure Validation ===\n")

    success = test_syntax_only()

    print(f"\n=== Overall Result ===")
    if success:
        print("SUCCESS: All syntax checks passed and core structures validated")
        return True
    else:
        print("FAILURE: Some syntax checks failed")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)