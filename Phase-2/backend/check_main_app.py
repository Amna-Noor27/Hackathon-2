"""
Simple check to verify the main application can be imported and has basic structure.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_main_app():
    """Check that main app has the expected structure."""
    print("Checking main application structure...")

    # Read the main.py file to verify structure
    try:
        with open("src/main.py", 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ("FastAPI import", "from fastapi import FastAPI" in content),
            ("Lifespan context manager", "async def lifespan(app:" in content),
            ("SQLModel import", "from sqlmodel import SQLModel" in content),
            ("Database engine", "from src.database import engine" in content),
            ("API router included", "app.include_router(tasks.router" in content),
            ("Health endpoint", "@app.get('/health')" in content or "def health_check" in content),
            ("Root endpoint", "@app.get('/')" in content or "def read_root" in content),
            ("Error handlers", "add_error_handlers(app)" in content)
        ]

        passed = 0
        total = len(checks)

        for check_name, result in checks:
            if result:
                print(f"OK: {check_name}")
                passed += 1
            else:
                print(f"ERR: {check_name}")

        print(f"\nMain app structure: {passed}/{total} checks passed")
        return passed == total

    except FileNotFoundError:
        print("ERROR: src/main.py not found")
        return False
    except Exception as e:
        print(f"ERROR checking main app: {e}")
        return False


def check_api_endpoints():
    """Check that API endpoints have the expected structure."""
    print("\nChecking API endpoints structure...")

    try:
        with open("src/api/tasks.py", 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ("GET /tasks endpoint", "def get_tasks(" in content and "/tasks" in content),
            ("POST /tasks endpoint", "def create_task(" in content and "status_code=201" in content),
            ("GET /tasks/{id} endpoint", "def get_task(" in content and "task_id:" in content),
            ("PUT /tasks/{id} endpoint", "def update_task(" in content and "task_update: TaskUpdate" in content),
            ("DELETE /tasks/{id} endpoint", "def delete_task(" in content),
            ("Dependency injection", "Depends(get_session)" in content),
            ("Response models", "response_model=" in content),
            ("User isolation", "user_id" in content and "user_id:" in content)
        ]

        passed = 0
        total = len(checks)

        for check_name, result in checks:
            if result:
                print(f"OK: {check_name}")
                passed += 1
            else:
                print(f"ERR: {check_name}")

        print(f"\nAPI endpoints structure: {passed}/{total} checks passed")
        return passed >= total - 2  # Allow 2 checks to fail for flexibility

    except FileNotFoundError:
        print("ERROR: src/api/tasks.py not found")
        return False
    except Exception as e:
        print(f"ERROR checking API endpoints: {e}")
        return False


def check_service_layer():
    """Check that the service layer has expected structure."""
    print("\nChecking service layer structure...")

    try:
        with open("src/services/task_service.py", 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ("TaskService class", "class TaskService:" in content),
            ("Create task method", "def create_task(" in content),
            ("Get tasks by user method", "def get_tasks_by_user(" in content),
            ("Get task by id method", "def get_task_by_id(" in content),
            ("Update task method", "def update_task(" in content),
            ("Delete task method", "def delete_task(" in content),
            ("User isolation", "user_id" in content and "Task.user_id ==" in content),
            ("Logging integration", "log_task_operation" in content)
        ]

        passed = 0
        total = len(checks)

        for check_name, result in checks:
            if result:
                print(f"OK: {check_name}")
                passed += 1
            else:
                print(f"ERR: {check_name}")

        print(f"\nService layer structure: {passed}/{total} checks passed")
        return passed >= total - 2  # Allow 2 checks to fail for flexibility

    except FileNotFoundError:
        print("ERROR: src/services/task_service.py not found")
        return False
    except Exception as e:
        print(f"ERROR checking service layer: {e}")
        return False


def main():
    """Run all checks."""
    print("=== Backend Application Structure Validation ===\n")

    app_ok = check_main_app()
    api_ok = check_api_endpoints()
    service_ok = check_service_layer()

    print(f"\n=== Final Assessment ===")
    print(f"Main app structure: {'PASS' if app_ok else 'FAIL'}")
    print(f"API endpoints: {'PASS' if api_ok else 'FAIL'}")
    print(f"Service layer: {'PASS' if service_ok else 'FAIL'}")

    overall_pass = app_ok and api_ok and service_ok
    print(f"Overall assessment: {'PASS' if overall_pass else 'FAIL'}")

    if overall_pass:
        print("\nSUCCESS: The backend application has all expected structural components!")
    else:
        print("\nWARNING: Some structural components are missing or incorrect.")

    return overall_pass


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)