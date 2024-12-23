from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CoursesBase(BaseModel):
    title: str
    description: str
    difficulty_id: UUID
    picture_id: Optional[UUID]  

class CoursesCreate(CoursesBase):
    pass

class Courses(CoursesBase):
    id: UUID

