import pytest
from src.models.task import Task, TaskCreate
from src.models.user import User, UserCreate
from datetime import datetime


def test_task_creation():
    """Test creating a task model."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "user_id": "user123"
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.completed is False
    assert task.user_id == "user123"
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_user_creation():
    """Test creating a user model."""
    user_data = {
        "email": "test@example.com"
    }

    user = User(**user_data)

    assert user.email == "test@example.com"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_task_create_schema():
    """Test the TaskCreate schema."""
    task_create_data = {
        "title": "New Task",
        "description": "Description for new task",
        "user_id": "user123"
    }

    task_create = TaskCreate(**task_create_data)

    assert task_create.title == "New Task"
    assert task_create.description == "Description for new task"
    assert task_create.user_id == "user123"