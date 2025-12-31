from datetime import datetime
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    is_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool | None = None
