from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.database import get_session
from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import task_service
from src.models.user import User
from src.auth.deps import get_current_user_id

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user.

    Security: This endpoint ensures that users can only access tasks associated with their account.
    The user_id is extracted from the verified JWT token and used to filter tasks.
    """
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access tasks"
        )

    tasks = task_service.get_tasks_by_user(session=session, user_id=current_user_id)
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Security: This endpoint ensures that tasks can only be created for the authenticated user.
    The user_id is extracted from the verified JWT token and used to associate the task.
    Users cannot create tasks for other users.
    """
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to create tasks"
        )

    # Validate the task data before creation
    if not task_create.title or len(task_create.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is required"
        )

    # Create the task with the authenticated user ID
    try:
        task = task_service.create_task(
            session=session,
            task_create=task_create,
            user_id=current_user_id
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID.

    Security: This endpoint ensures that users can only access tasks that belong to them.
    The user_id from the JWT token is validated against the task's user_id.
    """
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access task"
        )

    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task ID is required"
        )

    task = task_service.get_task_by_id(session=session, task_id=task_id, user_id=current_user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user")
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task.

    Security: This endpoint ensures that users can only update tasks that belong to them.
    The user_id from the JWT token is validated against the task's user_id.
    """
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to update task"
        )

    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task ID is required"
        )

    updated_task = task_service.update_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id,
        task_update=task_update
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user")
    return updated_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.

    Security: This endpoint ensures that users can only delete tasks that belong to them.
    The user_id from the JWT token is validated against the task's user_id.
    """
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to delete task"
        )

    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task ID is required"
        )

    deleted = task_service.delete_task(session=session, task_id=task_id, user_id=current_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to the user")
    return {"message": "Task deleted successfully"}