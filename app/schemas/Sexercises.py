from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ExercisesBase(BaseModel):
    title: Optional[str] = None
    done: bool
    course_id: UUID
    picture_id: UUID

    class Config:
        from_attributes = True

class ExercisesCreate(ExercisesBase):
    pass

class Exercises(ExercisesBase):
    id: UUID

    class Config:
        from_attributes = True
