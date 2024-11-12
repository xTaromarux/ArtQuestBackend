from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ProgressesBase(BaseModel):
    stage: int
    user_id: UUID
    user_course_id: UUID

    class Config:
        from_attributes = True

class ProgressesCreate(ProgressesBase):
    pass

class Progresses(ProgressesBase):
    id: UUID

    class Config:
        from_attributes = True
