from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PostBase(BaseModel):
    name: str
    thread_id: int
    
class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    name: Optional[str] = None
    thread_id: Optional[int] = None

class ThreadBase(BaseModel):
    name: str

class ThreadUpdate(ThreadBase):
    name: Optional[str] = None

class Thread(ThreadBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ThreadCreate(ThreadBase):
    pass