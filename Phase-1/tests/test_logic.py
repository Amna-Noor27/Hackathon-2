import pytest
from src.logic import tasks_db, next_id, add_task, list_tasks, toggle_task_status, delete_task, update_task

def test_update_task():
    add_task("T1")
    success = update_task(1, title="New", description="Desc")
    assert success is True
    assert tasks_db[0].title == "New"
    assert tasks_db[0].description == "Desc"
    assert update_task(99, title="X") is False

def test_toggle_task_status():
    task = add_task("T1")
    assert task.status == "Pending"
    success = toggle_task_status(1)
    assert success is True
    assert task.status == "Completed"
    toggle_task_status(1)
    assert task.status == "Pending"

def test_delete_task():
    add_task("T1")
    success = delete_task(1)
    assert success is True
    assert len(tasks_db) == 0
    assert delete_task(99) is False

@pytest.fixture(autouse=True)
def clear_db():
    """Clear the in-memory database before each test."""
    tasks_db.clear()
    import src.logic
    src.logic.next_id = 1

def test_add_task():
    task = add_task("Test Task", "Test Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert len(tasks_db) == 1

def test_list_tasks():
    add_task("T1", "D1")
    add_task("T2", "D2")
    tasks = list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "T1"
    assert tasks[1].title == "T2"
