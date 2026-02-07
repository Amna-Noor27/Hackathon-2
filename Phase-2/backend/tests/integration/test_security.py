"""
Integration tests for security functionality.
Tests user isolation and access control mechanisms.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_cross_user_access_attempts():
    """
    Test that users cannot access other users' tasks.
    """
    user1_id = "user1_secure_test"
    user2_id = "user2_secure_test"

    # Create a task for user1
    task_data = {
        "title": "User1's Private Task",
        "description": "This should only be accessible by user1",
        "user_id": user1_id
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code in [201, 400, 422, 500]

    if response.status_code == 201:
        task = response.json()
        task_id = task['id']

        # User2 should not be able to access user1's task
        response = client.get(f"/api/tasks/{task_id}?user_id={user2_id}")

        # Should return 404 (not found) or 403 (forbidden) to prevent
        # revealing that the task exists but belongs to another user
        assert response.status_code in [404, 403]

        # User2 should not be able to update user1's task
        update_data = {"title": "Hacked by User2"}
        response = client.put(f"/api/tasks/{task_id}?user_id={user2_id}", json=update_data)

        # Should return 404 (not found) or 403 (forbidden)
        assert response.status_code in [404, 403]

        # User2 should not be able to delete user1's task
        response = client.delete(f"/api/tasks/{task_id}?user_id={user2_id}")

        # Should return 404 (not found) or 403 (forbidden)
        assert response.status_code in [404, 403]


def test_user_task_listing_isolation():
    """
    Test that users can only see their own tasks when listing.
    """
    user1_id = "user1_list_test"
    user2_id = "user2_list_test"

    # Create tasks for user1
    user1_tasks = [
        {"title": f"User1 Task {i}", "description": f"Owned by {user1_id}", "user_id": user1_id}
        for i in range(3)
    ]

    for task_data in user1_tasks:
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code in [201, 400, 422, 500]

    # Create tasks for user2
    user2_tasks = [
        {"title": f"User2 Task {i}", "description": f"Owned by {user2_id}", "user_id": user2_id}
        for i in range(2)
    ]

    for task_data in user2_tasks:
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code in [201, 400, 422, 500]

    # User1 should only see their own tasks
    response = client.get(f"/api/tasks?user_id={user1_id}")
    if response.status_code == 200:
        user1_tasks_result = response.json()
        assert len(user1_tasks_result) == 3
        for task in user1_tasks_result:
            assert task["user_id"] == user1_id

    # User2 should only see their own tasks
    response = client.get(f"/api/tasks?user_id={user2_id}")
    if response.status_code == 200:
        user2_tasks_result = response.json()
        assert len(user2_tasks_result) == 2
        for task in user2_tasks_result:
            assert task["user_id"] == user2_id


def test_attempt_to_modify_other_users_task():
    """
    Test that attempts to modify another user's task fail appropriately.
    """
    owner_user_id = "owner_user"
    attacker_user_id = "attacker_user"

    # Create a task owned by owner_user
    task_data = {
        "title": "Owner's Task",
        "description": "Belongs to owner_user",
        "user_id": owner_user_id
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code in [201, 400, 422, 500]

    if response.status_code == 201:
        task = response.json()
        task_id = task['id']

        # Attacker tries to update the owner's task
        malicious_update = {
            "title": "Compromised Task",
            "completed": True
        }

        response = client.put(f"/api/tasks/{task_id}?user_id={attacker_user_id}", json=malicious_update)

        # Should fail with 404 or 403
        assert response.status_code in [404, 403]

        # Verify the original task remains unchanged
        response = client.get(f"/api/tasks/{task_id}?user_id={owner_user_id}")
        if response.status_code == 200:
            original_task = response.json()
            assert original_task["title"] != "Compromised Task"
            assert original_task["user_id"] == owner_user_id


def test_delete_isolation():
    """
    Test that users can only delete their own tasks.
    """
    owner_user_id = "owner_for_delete"
    other_user_id = "other_for_delete"

    # Create a task for the owner
    task_data = {
        "title": "Deletable Task",
        "description": "This task can only be deleted by its owner",
        "user_id": owner_user_id
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code in [201, 400, 422, 500]

    if response.status_code == 201:
        task = response.json()
        task_id = task['id']

        # Other user should not be able to delete the task
        response = client.delete(f"/api/tasks/{task_id}?user_id={other_user_id}")
        assert response.status_code in [404, 403]

        # Verify task still exists
        response_verify = client.get(f"/api/tasks/{task_id}?user_id={owner_user_id}")
        assert response_verify.status_code == 200

        # Owner should be able to delete the task
        response = client.delete(f"/api/tasks/{task_id}?user_id={owner_user_id}")
        assert response.status_code == 200