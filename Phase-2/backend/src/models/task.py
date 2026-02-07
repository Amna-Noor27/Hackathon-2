from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item.
    NOTE: user_id references the user ID from Better Auth's users table.
    While we cannot create a traditional foreign key constraint to Better Auth's
    external users table, this column stores the user_id from JWT tokens
    issued by Better Auth for association.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(nullable=False, description="Reference to Better Auth user ID")  # Foreign key reference to Better Auth user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    # user_id will be set from the authenticated user, not from the request


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    # user_id should not be updated, as it represents ownership


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: str
    user_id: str  # Include user_id in the response
    created_at: datetime
    updated_at: datetime