from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    """Base user model with common fields"""
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    email_verified: Optional[datetime] = Field(default=None)  # Better Auth requirement
    image: Optional[str] = Field(default=None)  # Better Auth requirement


class User(UserBase, table=True):
    """User model for Better Auth compatibility"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    # Hashed password database mein save karne ke liye
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Model for creating new users"""
    # Frontend se aane wala plain password
    password: str


class UserRead(UserBase):
    """Model for reading user data"""
    id: str
    created_at: datetime
    updated_at: datetime


class SessionBase(SQLModel):
    """Base session model"""
    user_id: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)


class Session(SessionBase, table=True):
    """Session model for Better Auth compatibility"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AccountBase(SQLModel):
    """Base account model for third-party providers"""
    user_id: str = Field(nullable=False)
    provider_id: str = Field(nullable=False)
    provider_user_id: str = Field(nullable=False)
    access_token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    id_token: Optional[str] = Field(default=None)
    token_type: Optional[str] = Field(default=None)
    scope: Optional[str] = Field(default=None)
    expires_at: Optional[int] = Field(default=None)


class Account(AccountBase, table=True):
    """Account model for Better Auth compatibility"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SessionCreate(SessionBase):
    """Model for creating new sessions"""
    pass


class AccountCreate(AccountBase):
    """Model for creating new accounts"""
    pass