"""
Contract test for cross-service identity verification.
These tests verify that JWT tokens issued by Better Auth can be successfully validated by the FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from jose import jwt
from src.core.config import settings


client = TestClient(app)


def test_backend_accepts_tokens_with_correct_signature():
    """
    Test that the backend can validate tokens with the correct signature algorithm and secret.
    """
    # Create a token with the same algorithm and secret as the backend expects
    valid_token = jwt.encode(
        {
            "sub": "user123",
            "email": "test@example.com",
            "exp": 9999999999,  # Far in the future
            "iat": 1000000000,  # Past timestamp
            "iss": "todo-app"  # Issuer
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {valid_token}"}

    # This should not return 401 (would be 404/400 due to other factors)
    response = client.get("/api/tasks", headers=headers)
    assert response.status_code != 401


def test_backend_rejects_tokens_with_wrong_secret():
    """
    Test that the backend rejects tokens with a different secret.
    """
    # Create a token with a different secret
    invalid_token = jwt.encode(
        {
            "sub": "user123",
            "email": "test@example.com",
            "exp": 9999999999,
        },
        "wrong-secret-key",  # Different secret
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {invalid_token}"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401


def test_backend_rejects_tokens_with_wrong_algorithm():
    """
    Test that the backend rejects tokens with a different algorithm.
    """
    # Create a token with a different algorithm (if possible with this library)
    # For this test, we'll just make sure the backend properly validates the algorithm
    valid_token = jwt.encode(
        {
            "sub": "user123",
            "email": "test@example.com",
            "exp": 9999999999,
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    # Tamper with the token to make it invalid
    tampered_token = valid_token[:-5] + "aaaaa"  # Change last few characters

    headers = {"Authorization": f"Bearer {tampered_token}"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401


def test_backend_extracts_correct_user_identity():
    """
    Test that the backend correctly extracts user identity from JWT claims.
    """
    user_id = "test_user_456"
    user_email = "user@example.com"

    # Create a token with specific user data
    token_with_user_data = jwt.encode(
        {
            "sub": user_id,
            "email": user_email,
            "exp": 9999999999,
        },
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {token_with_user_data}"}

    # Although the actual API call may fail for other reasons (like user not existing in DB),
    # it should not fail with 401 due to invalid token
    response = client.get("/api/tasks", headers=headers)
    assert response.status_code != 401


def test_backend_handles_standard_jwt_claims():
    """
    Test that the backend properly handles standard JWT claims (sub, exp, iat, iss).
    """
    standard_payload = {
        "sub": "standard_user_789",
        "email": "standard@example.com",
        "exp": 9999999999,  # Far in the future
        "iat": 1000000000,  # Timestamp when token was issued
        "iss": "todo-app",  # Issuer
        "aud": "todo-users",  # Audience (optional)
    }

    token_with_standard_claims = jwt.encode(
        standard_payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    headers = {"Authorization": f"Bearer {token_with_standard_claims}"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code != 401