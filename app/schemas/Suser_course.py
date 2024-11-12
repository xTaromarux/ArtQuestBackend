from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserCourseBase(BaseModel):
    course_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

class UserCourseCreate(UserCourseBase):
    pass

class UserCourseUpdate(UserCourseBase):
    pass

class UserCourse(UserCourseBase):
    id: UUID

    class Config:
        from_attributes = True
