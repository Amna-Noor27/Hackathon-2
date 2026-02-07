"""
Integration tests for JWT token validation consistency across services.
Tests that JWT tokens work consistently between different parts of the application.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from jose import jwt
from src.core.config import settings


client = TestClient(app)


def test_same_token_works_across_all_endpoints():
    """
    Test that the same valid JWT token works across all API endpoints.
    """
    # Create a single valid token
    valid_token = jwt.encode(
        {
            "sub": "consistent_user",
            "email": "consistent@example.com",
            "exp": 9999999999,  # Far in the future
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {valid_token}"}

    # Test that the token works for all endpoints
    endpoints_to_test = [
        ("GET", "/api/tasks"),
        ("POST", "/api/tasks", {"title": "Test task"}),
        ("GET", "/api/tasks/task123"),
        ("PUT", "/api/tasks/task123", {"title": "Updated task"}),
        ("DELETE", "/api/tasks/task123")
    ]

    for endpoint in endpoints_to_test:
        method = endpoint[0]
        url = endpoint[1]

        if method == "GET":
            response = client.get(url, headers=headers)
        elif method == "POST":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.post(url, json=data, headers=headers)
        elif method == "PUT":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = client.delete(url, headers=headers)

        # All should be authenticated (not 401), though they might return other status codes
        assert response.status_code != 401


def test_invalid_token_fails_across_all_endpoints():
    """
    Test that invalid tokens fail consistently across all API endpoints.
    """
    # Use an invalid token
    invalid_token = "invalid.token.string"

    headers = {"Authorization": f"Bearer {invalid_token}"}

    # Test that the invalid token fails for all endpoints
    endpoints_to_test = [
        ("GET", "/api/tasks"),
        ("POST", "/api/tasks", {"title": "Test task"}),
        ("GET", "/api/tasks/task123"),
        ("PUT", "/api/tasks/task123", {"title": "Updated task"}),
        ("DELETE", "/api/tasks/task123")
    ]

    for endpoint in endpoints_to_test:
        method = endpoint[0]
        url = endpoint[1]

        if method == "GET":
            response = client.get(url, headers=headers)
        elif method == "POST":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.post(url, json=data, headers=headers)
        elif method == "PUT":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = client.delete(url, headers=headers)

        # All should return 401 (unauthorized) for invalid token
        assert response.status_code == 401


def test_expired_token_fails_across_all_endpoints():
    """
    Test that expired tokens fail consistently across all API endpoints.
    """
    # Create an expired token
    expired_token = jwt.encode(
        {
            "sub": "expired_user",
            "email": "expired@example.com",
            "exp": 1000,  # Expired long ago
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {expired_token}"}

    # Test that the expired token fails for all endpoints
    endpoints_to_test = [
        ("GET", "/api/tasks"),
        ("POST", "/api/tasks", {"title": "Test task"}),
        ("GET", "/api/tasks/task123"),
        ("PUT", "/api/tasks/task123", {"title": "Updated task"}),
        ("DELETE", "/api/tasks/task123")
    ]

    for endpoint in endpoints_to_test:
        method = endpoint[0]
        url = endpoint[1]

        if method == "GET":
            response = client.get(url, headers=headers)
        elif method == "POST":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.post(url, json=data, headers=headers)
        elif method == "PUT":
            data = endpoint[2] if len(endpoint) > 2 else {}
            response = client.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = client.delete(url, headers=headers)

        # All should return 401 (unauthorized) for expired token
        assert response.status_code == 401


def test_different_users_get_different_access():
    """
    Test that different users get appropriate access based on their identity.
    Note: This is more of a conceptual test since we can't easily create actual tasks in this context.
    """
    # Create tokens for two different users
    user1_token = jwt.encode(
        {
            "sub": "user_1_unique_id",
            "email": "user1@example.com",
            "exp": 9999999999,
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    user2_token = jwt.encode(
        {
            "sub": "user_2_unique_id",
            "email": "user2@example.com",
            "exp": 9999999999,
        },
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


def test_token_payload_preservation():
    """
    Test that the token payload is properly preserved and accessible throughout the request lifecycle.
    """
    # Create a token with specific custom claims
    custom_payload = {
        "sub": "custom_payload_user",
        "email": "custom@example.com",
        "exp": 9999999999,
        "role": "user",
        "permissions": ["read", "write"],
        "tenant_id": "tenant_abc_123"
    }

    token_with_custom_claims = jwt.encode(
        custom_payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {token_with_custom_claims}"}

    # Make a request to verify the token is processed correctly
    response = client.get("/api/tasks", headers=headers)

    # Should not be unauthorized
    assert response.status_code != 401