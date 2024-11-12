from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ExercisesBase(BaseModel):
    title: str
    description: str
    aipart: Optional[str] = None
    colSpan: Optional[int] = None
    rowSpan: Optional[int] = None
    cols: Optional[int] = None
    rows: Optional[int] = None
    difficulty_id: UUID

    class Config:
        from_attributes = True

class ExercisesCreate(ExercisesBase):
    pass

class Exercises(ExercisesBase):
    id: UUID

    class Config:
        from_attributes = True
