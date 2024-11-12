from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CoursesBase(BaseModel):
    title: str
    description: str
    difficulty_id: UUID
    picture_id: UUID

    class Config:
        from_attributes = True

class CoursesCreate(CoursesBase):
    pass

class Courses(CoursesBase):
    id: UUID

    class Config:
        from_attributes = True
