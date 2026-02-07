"""
Contract tests for JWT validation functionality.
These tests verify that the API endpoints properly validate JWT tokens.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from jose import jwt
from src.core.config import settings

client = TestClient(app)


def test_unauthorized_access_without_token():
    """
    Test that requests without a JWT token return 401 Unauthorized.
    """
    response = client.get("/api/tasks")
    assert response.status_code == 401

    response = client.post("/api/tasks", json={"title": "Test task"})
    assert response.status_code == 401

    response = client.get("/api/tasks/task123")
    assert response.status_code == 401

    response = client.put("/api/tasks/task123", json={"title": "Updated task"})
    assert response.status_code == 401

    response = client.delete("/api/tasks/task123")
    assert response.status_code == 401


def test_unauthorized_access_with_invalid_token():
    """
    Test that requests with an invalid JWT token return 401 Unauthorized.
    """
    headers = {"Authorization": "Bearer invalid-token"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401

    response = client.post("/api/tasks", json={"title": "Test task"}, headers=headers)
    assert response.status_code == 401

    response = client.get("/api/tasks/task123", headers=headers)
    assert response.status_code == 401

    response = client.put("/api/tasks/task123", json={"title": "Updated task"}, headers=headers)
    assert response.status_code == 401

    response = client.delete("/api/tasks/task123", headers=headers)
    assert response.status_code == 401


def test_unauthorized_access_with_expired_token():
    """
    Test that requests with an expired JWT token return 401 Unauthorized.
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

    response = client.put("/api/tasks/task123", json={"title": "Updated task"}, headers=headers)
    assert response.status_code == 401

    response = client.delete("/api/tasks/task123", headers=headers)
    assert response.status_code == 401


def test_valid_token_allows_access():
    """
    Test that requests with a valid JWT token are processed successfully.
    """
    # Create a valid token
    valid_token = jwt.encode(
        {"sub": "user123", "exp": 9999999999},  # Expires far in the future
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {valid_token}"}

    # Note: These will fail due to other factors (like user not existing in DB),
    # but they should not fail with 401 Unauthorized
    response = client.get("/api/tasks", headers=headers)
    # Could be 200 (empty list) or 404/400 depending on implementation
    assert response.status_code != 401

    response = client.post("/api/tasks", json={"title": "Test task"}, headers=headers)
    # Could be 201 (created) or 400 (validation error), but not 401
    assert response.status_code != 401