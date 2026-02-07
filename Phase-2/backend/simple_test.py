"""
Simple test to verify that the main modules can be imported
without requiring all dependencies to be installed.
"""
import sys
import traceback


def test_imports():
    """Test importing the main modules."""
    modules_to_test = [
        "src.database",
        "src.models.user",
        "src.models.task",
        "src.services.task_service",
        "src.schemas.error",
        "src.core.config",
        "src.core.logging_config",
        "src.middleware.error_handler",
        "src.api.tasks"
    ]

    print("Testing module imports...")
    failed_imports = []

    for module in modules_to_test:
        try:
            # Replace dots with forward slashes to form file path
            parts = module.split('.')
            file_path = '/'.join(parts) + '.py'

            # Import the module using importlib
            import importlib.util
            spec = importlib.util.spec_from_file_location(module, f"{module.replace('.', '/')}.py")
            if spec and spec.loader:
                imported_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(imported_module)
                print(f"✓ {module} - Imported successfully")
            else:
                # Alternative approach: add src to path and import
                sys.path.insert(0, 'src')
                imported_module = __import__(module, fromlist=[''])
                print(f"OK: {module} - Imported successfully")
        except ImportError as e:
            failed_imports.append((module, str(e)))
            print(f"ERR: {module} - Import failed: {e}")
        except Exception as e:
            failed_imports.append((module, str(e)))
            print(f"ERR: {module} - Error: {e}")

    return len(failed_imports) == 0


def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    try:
        # Import models
        sys.path.insert(0, 'src')
        from models.task import TaskCreate

        # Test creating a simple task object
        task_data = {
            "title": "Test Task",
            "description": "This is a test",
            "user_id": "test_user_123"
        }

        task_create = TaskCreate(**task_data)
        print(f"OK: TaskCreate model - Created successfully: {task_create.title}")

        # Import user model
        from models.user import UserCreate
        user_data = {"email": "test@example.com"}
        user_create = UserCreate(**user_data)
        print(f"OK: UserCreate model - Created successfully: {user_create.email}")

        return True
    except Exception as e:
        print(f"ERR: Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=== Simple Backend Module Test ===\n")

    print("1. Testing module imports:")
    imports_ok = test_imports()

    print("\n2. Testing basic functionality:")
    functionality_ok = test_basic_functionality()

    print(f"\n=== Test Summary ===")
    print(f"Module imports: {'PASS' if imports_ok else 'FAIL'}")
    print(f"Basic functionality: {'PASS' if functionality_ok else 'FAIL'}")

    overall_success = imports_ok and functionality_ok
    print(f"Overall result: {'SUCCESS' if overall_success else 'FAILURE'}")

    return overall_success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)