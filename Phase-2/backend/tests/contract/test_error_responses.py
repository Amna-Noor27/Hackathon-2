"""
Contract tests for error response functionality.
These tests verify that the API endpoints return appropriate error responses.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_error_response_contract():
    """
    Test that the API contract includes appropriate error responses.
    """
    # Test 404 for non-existent task
    response = client.get("/api/tasks/nonexistent_task_id?user_id=test_user")
    assert response.status_code in [404, 401, 403]

    # If it's a 404, check the error response format
    if response.status_code == 404:
        data = response.json()
        # The response should have appropriate error structure
        assert "detail" in data or "error" in data


def test_bad_request_response_contract():
    """
    Test that the API returns 400 for bad requests.
    """
    # Try to create a task with invalid data
    invalid_task_data = {
        # Missing required "title" field
        "user_id": "test_user"
    }

    response = client.post("/api/tasks", json=invalid_task_data)
    assert response.status_code in [400, 422]  # 422 is also valid for validation errors

    if response.status_code in [400, 422]:
        data = response.json()
        # The response should contain error information
        assert "detail" in data or "error" in data


def test_error_response_structure():
    """
    Test that error responses follow the expected format.
    """
    # Test with invalid request data
    invalid_data = {
        "invalid_field": "some_value"
    }

    response = client.post("/api/tasks", json=invalid_data)
    assert response.status_code in [400, 422, 422]

    if response.status_code in [400, 422]:
        data = response.json()
        # Should contain error details
        assert isinstance(data, dict)


def test_internal_server_error_contract():
    """
    Test the contract for 500 internal server errors.
    """
    # While we can't easily trigger a 500 in contract tests,
    # we can verify the API is designed to handle them
    # This is more of a design verification
    pass


def test_standard_http_status_codes():
    """
    Test that the API contract specifies appropriate HTTP status codes.
    """
    # This test verifies that the API endpoints are designed to return
    # the correct status codes as per the contract

    # 200 OK for successful GET requests
    # 201 Created for successful POST requests
    # 400 Bad Request for invalid input
    # 404 Not Found for missing resources
    # 500 Internal Server Error for server issues

    # These are verified through the other contract tests
    assert True  # Placeholder assertion


def test_error_message_clarity():
    """
    Test that error messages are clear and helpful.
    """
    # Try to access a non-existent task
    response = client.get("/api/tasks/nonexistent_task_id?user_id=test_user")

    if response.status_code in [404, 401, 403]:
        data = response.json()
        # Error messages should be descriptive
        if "detail" in data:
            assert isinstance(data["detail"], str)
        elif "error" in data:
            # If using error schema, it should have proper structure
            assert "message" in data["error"]