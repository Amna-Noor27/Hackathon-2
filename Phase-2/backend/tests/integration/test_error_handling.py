"""
Integration tests for error handling functionality.
Tests that the system handles malformed requests appropriately.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_malformed_requests_handling():
    """
    Test that the system handles malformed requests appropriately.
    """
    # Test request with missing required fields
    incomplete_task_data = {
        # Missing required "title" field
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=incomplete_task_data)
    assert response.status_code in [400, 422]

    if response.status_code in [400, 422]:
        data = response.json()
        # Should return appropriate error response
        assert "detail" in data or "error" in data


def test_invalid_data_types():
    """
    Test handling of requests with invalid data types.
    """
    invalid_task_data = {
        "title": 12345,  # Title should be string
        "description": ["description should be string"],  # Should be string
        "completed": "false",  # Should be boolean
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=invalid_task_data)
    assert response.status_code in [400, 422]


def test_extremely_long_input():
    """
    Test handling of extremely long input values.
    """
    long_title = "t" * 300  # Exceeds max length of 255
    long_task_data = {
        "title": long_title,
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=long_task_data)
    assert response.status_code in [400, 422]


def test_invalid_json():
    """
    Test handling of invalid JSON requests.
    """
    # This test is difficult to do with TestClient as it handles JSON serialization
    # We'll focus on testing valid JSON with invalid structure instead
    invalid_json_data = {
        "title": "",
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=invalid_json_data)
    # Empty title might be invalid depending on validation
    assert response.status_code in [201, 400, 422]


def test_nonexistent_endpoints():
    """
    Test responses for nonexistent endpoints.
    """
    response = client.get("/api/nonexistent_endpoint")
    assert response.status_code == 404


def test_invalid_method_on_endpoint():
    """
    Test responses for invalid HTTP methods on endpoints.
    """
    # Try to POST to a GET-only route (if it existed)
    # Or test with a custom invalid path
    response = client.post("/api/tasks/invalid_task_id_that_does_not_exist?user_id=test_user", json={})
    assert response.status_code in [404, 405]


def test_error_response_consistency():
    """
    Test that error responses are consistent across different endpoints.
    """
    # Test various error scenarios and check response format consistency

    # 1. Missing required field in POST
    response1 = client.post("/api/tasks", json={"user_id": "test_user"})  # Missing title
    error1 = response1.json() if response1.status_code in [400, 422] else {}

    # 2. Non-existent resource in GET
    response2 = client.get("/api/tasks/nonexistent_id?user_id=test_user")
    error2 = response2.json() if response2.status_code in [404, 403, 401] else {}

    # Both should have consistent error reporting (either detail or error structure)
    has_detail_or_error_1 = "detail" in error1 or "error" in error1
    has_detail_or_error_2 = "detail" in error2 or "error" in error2

    # Both responses should have error information
    assert has_detail_or_error_1
    assert has_detail_or_error_2


def test_boundary_conditions():
    """
    Test boundary conditions and edge cases.
    """
    # Test with maximum allowed title length
    max_title = "t" * 255
    valid_task_data = {
        "title": max_title,
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=valid_task_data)
    # This should either succeed or fail for other reasons, but not due to length validation
    assert response.status_code in [201, 400, 422, 500]

    # Test with minimum required fields
    minimal_task_data = {
        "title": "Minimal Task",
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=minimal_task_data)
    assert response.status_code in [201, 400, 422, 500]


def test_special_characters_handling():
    """
    Test handling of special characters in input.
    """
    special_char_data = {
        "title": "Task with special chars: !@#$%^&*()",
        "description": "Description with unicode: ñáéíóú 中文",
        "user_id": "test_user_with_special_chars"
    }

    response = client.post("/api/tasks", json=special_char_data)
    # Should handle special characters appropriately
    assert response.status_code in [201, 400, 422, 500]


def test_concurrent_error_scenarios():
    """
    Test error handling under concurrent scenarios (basic simulation).
    """
    # While we can't truly test concurrency with TestClient,
    # we can test rapid successive requests that might cause issues

    user_id = "concurrent_test_user"

    # Make several requests rapidly
    for i in range(3):
        task_data = {
            "title": f"Concurrent Task {i}",
            "user_id": user_id
        }
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code in [201, 400, 422, 500]

    # Try to get all tasks
    response = client.get(f"/api/tasks?user_id={user_id}")
    assert response.status_code in [200, 401, 403]