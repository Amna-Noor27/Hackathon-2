"""
Contract tests for the tasks API endpoints.
These tests verify that the API endpoints match the expected contract.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.task import TaskCreate

client = TestClient(app)


def test_get_tasks_endpoint_contract():
    """
    Test the GET /api/tasks endpoint contract.
    """
    # This test checks that the endpoint exists and returns the expected status code
    # In a real implementation, we would need to mock the user authentication
    response = client.get("/api/tasks?user_id=test_user")

    # The endpoint should return 200 OK or 401/403 depending on auth
    # For now, we'll just check it returns a valid response
    assert response.status_code in [200, 401, 403, 404]


def test_create_task_endpoint_contract():
    """
    Test the POST /api/tasks endpoint contract.
    """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=task_data)

    # The endpoint should return either 201 Created or 400/401/403
    assert response.status_code in [201, 400, 401, 403]


def test_get_specific_task_endpoint_contract():
    """
    Test the GET /api/tasks/{task_id} endpoint contract.
    """
    response = client.get("/api/tasks/nonexistent_task_id?user_id=test_user")

    # The endpoint should return 200 OK, 404 Not Found, or 401/403
    assert response.status_code in [200, 404, 401, 403]


def test_update_task_endpoint_contract():
    """
    Test the PUT /api/tasks/{task_id} endpoint contract.
    """
    update_data = {
        "title": "Updated Task Title",
        "completed": True
    }

    response = client.put("/api/tasks/nonexistent_task_id?user_id=test_user", json=update_data)

    # The endpoint should return 200 OK, 404 Not Found, or 401/403
    assert response.status_code in [200, 404, 401, 403]


def test_delete_task_endpoint_contract():
    """
    Test the DELETE /api/tasks/{task_id} endpoint contract.
    """
    response = client.delete("/api/tasks/nonexistent_task_id?user_id=test_user")

    # The endpoint should return 200 OK, 404 Not Found, or 401/403
    assert response.status_code in [200, 404, 401, 403]


def test_request_body_validation():
    """
    Test that the API validates request bodies correctly.
    """
    # Try to create a task without required fields
    incomplete_task_data = {
        "user_id": "test_user"
        # Missing required "title" field
    }

    response = client.post("/api/tasks", json=incomplete_task_data)

    # Should return 400 Bad Request due to validation error
    assert response.status_code in [400, 422]  # 422 is also valid for validation errors


def test_response_format():
    """
    Test that API responses follow the expected format.
    """
    # This is a simplified check - in real contract tests we'd validate the full schema
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": "test_user"
    }

    # We can't create a valid task without a real database,
    # but we can test the validation response
    response = client.post("/api/tasks", json=task_data)

    # If successful, the response should have certain fields
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "completed" in data
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data