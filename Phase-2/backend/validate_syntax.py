"""
Simple validation script to check that all Python files have correct syntax.
"""
import ast
import os
from pathlib import Path


def validate_python_files(directory):
    """Validate syntax of all Python files in the given directory."""
    errors = []

    for py_file in Path(directory).rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the file to check for syntax errors
            ast.parse(content)
            print(f"OK: {py_file} - Syntax OK")
        except SyntaxError as e:
            errors.append((str(py_file), str(e)))
            print(f"ERR: {py_file} - Syntax Error: {e}")
        except Exception as e:
            errors.append((str(py_file), str(e)))
            print(f"ERR: {py_file} - Error: {e}")

    return errors


def main():
    """Main validation function."""
    print("Validating Python files in backend/src...")
    errors = validate_python_files("src")

    print("\nValidating Python files in backend/tests...")
    test_errors = validate_python_files("tests")
    errors.extend(test_errors)

    print("\nValidating Python files in backend root...")
    root_errors = validate_python_files(".")
    errors.extend(root_errors)

    if errors:
        print(f"\nFAILED: Found {len(errors)} syntax error(s)")
        for file_path, error in errors:
            print(f"  - {file_path}: {error}")
        return False
    else:
        print("\nSUCCESS: All Python files have valid syntax!")
        return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)