from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AccountBase(SQLModel):
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
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime