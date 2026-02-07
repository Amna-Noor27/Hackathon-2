from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class SessionBase(SQLModel):
    user_id: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)

class Session(SessionBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SessionCreate(SessionBase):
    pass

class SessionRead(SessionBase):
    id: str
    created_at: datetime
    updated_at: datetime