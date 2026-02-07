from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "Pending"

# In-Memory Storage
tasks_db: List[Task] = []
next_id: int = 1

def add_task(title: str, description: str = "") -> Task:
    global next_id
    task = Task(id=next_id, title=title, description=description)
    tasks_db.append(task)
    next_id += 1
    return task

def list_tasks() -> List[Task]:
    return tasks_db

def toggle_task_status(task_id: int) -> bool:
    for task in tasks_db:
        if task.id == task_id:
            task.status = "Completed" if task.status == "Pending" else "Pending"
            return True
    return False

def delete_task(task_id: int) -> bool:
    global tasks_db
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return True
    return False

def update_task(task_id: int, title: str = None, description: str = None) -> bool:
    for task in tasks_db:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True
    return False
