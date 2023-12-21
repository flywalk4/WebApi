from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ThreadBase(BaseModel):
    name: str

class ThreadCreate(ThreadBase):
    pass

class ThreadUpdate(ThreadBase):
    name: Optional[str] = None

class Thread(ThreadBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class PostBase(BaseModel):
    name: str
    thread_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    name: Optional[str] = None
    thread_id: Optional[int] = None

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
