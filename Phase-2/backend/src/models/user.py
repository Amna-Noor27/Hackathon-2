from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    email_verified: Optional[datetime] = Field(default=None)  # Better Auth requirement
    image: Optional[str] = Field(default=None)  # Better Auth requirement

class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    # Hashed password database mein save karne ke liye
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    # Frontend se aane wala plain password
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime