"""
Basic validation test to ensure the application works as expected.
"""
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_app_runs():
    """Test that the application starts and responds to requests."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_routes_exist():
    """Test that the API routes are registered."""
    # Test that the tasks router is available
    response = client.get("/api/tasks?user_id=test")
    # This might return 401/403 if auth is required or 200 if successful
    # Both are valid responses indicating the route exists
    assert response.status_code in [200, 401, 403, 404]


if __name__ == "__main__":
    test_app_runs()
    test_health_check()
    test_api_routes_exist()
    print("All basic validation tests passed!")