from sqlmodel import Session, select
from typing import List, Optional
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from fastapi import HTTPException
from src.core.logging_config import log_task_operation


class TaskService:
    """
    Service class for handling task-related operations.
    """

    def create_task(self, *, session: Session, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for a user.
        """
        # Verify the user exists
        user = session.get(User, user_id)
        if not user:
            log_task_operation("create", user_id, success=False)
            raise HTTPException(status_code=404, detail="User not found")

        # Create the task with the validated data plus required fields
        # We need to exclude fields that have default factories to let SQLModel handle them
        task_data = task_create.model_dump()
        db_task = Task(
            **task_data,
            user_id=user_id  # Set user_id from authenticated user
            # id, created_at, and updated_at will be handled by the model's default factories
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_operation("create", user_id, db_task.id, success=True)
        return db_task

    def get_tasks_by_user(self, *, session: Session, user_id: str) -> List[Task]:
        """
        Get all tasks for a specific user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        log_task_operation("get_list", user_id, success=True)
        return tasks

    def get_task_by_id(self, *, session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID, ensuring it belongs to the user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if task:
            log_task_operation("get", user_id, task_id, success=True)
        else:
            log_task_operation("get", user_id, task_id, success=False)
        return task

    def update_task(self, *, session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a specific task, ensuring it belongs to the user.
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            log_task_operation("update", user_id, task_id, success=False)
            return None

        # Update the task with the provided values
        task_data = task_update.model_dump(exclude_unset=True)
        for field, value in task_data.items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_operation("update", user_id, task_id, success=True)
        return db_task

    def delete_task(self, *, session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a specific task, ensuring it belongs to the user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            log_task_operation("delete", user_id, task_id, success=False)
            return False

        session.delete(db_task)
        session.commit()
        log_task_operation("delete", user_id, task_id, success=True)
        return True


# Global instance of the service
task_service = TaskService()