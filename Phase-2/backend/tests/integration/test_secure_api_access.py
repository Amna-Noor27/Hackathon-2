"""
Integration tests for secure API access with JWT tokens.
Tests that authenticated users can access the API and unauthenticated users cannot.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from jose import jwt
from src.core.config import settings


client = TestClient(app)


def test_authenticated_user_can_access_api():
    """
    Test that an authenticated user with a valid JWT can access the API.
    """
    # Create a valid token for a user
    valid_token = jwt.encode(
        {"sub": "test_user_123", "exp": 9999999999},  # Expires far in the future
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {valid_token}"}

    # Try to access the tasks endpoint with the valid token
    response = client.get("/api/tasks", headers=headers)

    # The response should not be 401 (unauthorized)
    # It might be 200 (success) or 400/404 (other validation errors), but not 401
    assert response.status_code != 401


def test_unauthenticated_user_cannot_access_api():
    """
    Test that an unauthenticated user cannot access the protected API.
    """
    # Try to access the tasks endpoint without a token
    response = client.get("/api/tasks")
    assert response.status_code == 401

    # Try to create a task without a token
    response = client.post("/api/tasks", json={"title": "Test task"})
    assert response.status_code == 401

    # Try to access a specific task without a token
    response = client.get("/api/tasks/task123")
    assert response.status_code == 401

    # Try to update a task without a token
    response = client.put("/api/tasks/task123", json={"title": "Updated"})
    assert response.status_code == 401

    # Try to delete a task without a token
    response = client.delete("/api/tasks/task123")
    assert response.status_code == 401


def test_invalid_token_results_in_unauthorized():
    """
    Test that requests with invalid tokens return 401.
    """
    headers = {"Authorization": "Bearer invalid.token.here"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401

    response = client.post("/api/tasks", json={"title": "Test task"}, headers=headers)
    assert response.status_code == 401

    response = client.get("/api/tasks/task123", headers=headers)
    assert response.status_code == 401

    response = client.put("/api/tasks/task123", json={"title": "Updated"}, headers=headers)
    assert response.status_code == 401

    response = client.delete("/api/tasks/task123", headers=headers)
    assert response.status_code == 401


def test_expired_token_results_in_unauthorized():
    """
    Test that requests with expired tokens return 401.
    """
    # Create an expired token
    expired_token = jwt.encode(
        {"sub": "user123", "exp": 1000},  # Expired long ago
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {expired_token}"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401

    response = client.post("/api/tasks", json={"title": "Test task"}, headers=headers)
    assert response.status_code == 401

    response = client.get("/api/tasks/task123", headers=headers)
    assert response.status_code == 401

    response = client.put("/api/tasks/task123", json={"title": "Updated"}, headers=headers)
    assert response.status_code == 401

    response = client.delete("/api/tasks/task123", headers=headers)
    assert response.status_code == 401


def test_different_users_have_separate_access():
    """
    Test that users can only access their own tasks.
    Note: This test would require more complex setup to fully validate
    since it would require creating actual tasks in the database.
    """
    # Create tokens for two different users
    user1_token = jwt.encode(
        {"sub": "user1", "exp": 9999999999},
        settings.secret_key,
        algorithm=settings.algorithm
    )

    user2_token = jwt.encode(
        {"sub": "user2", "exp": 9999999999},
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers1 = {"Authorization": f"Bearer {user1_token}"}
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # Both users should be able to access the API (not get 401)
    response1 = client.get("/api/tasks", headers=headers1)
    response2 = client.get("/api/tasks", headers=headers2)

    # Both should be authenticated (not 401), though they may get different results
    assert response1.status_code != 401
    assert response2.status_code != 401