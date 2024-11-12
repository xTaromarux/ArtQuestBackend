from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ProgressBase(BaseModel):
    score: int
    description: Optional[str] = None
    user_id: UUID
    exercise_id: UUID

    class Config:
        from_attributes = True

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: UUID

    class Config:
        from_attributes = True
