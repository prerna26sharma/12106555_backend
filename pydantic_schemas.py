# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True  # Update this line

class BulkTasks(BaseModel):
    tasks: List[TaskCreate]
