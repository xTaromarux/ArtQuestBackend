from pydantic import BaseModel
from uuid import UUID

class UserCourseBase(BaseModel):
    course_id: UUID
    user_id: UUID

class UserCourseCreate(UserCourseBase):
    pass

class UserCourseUpdate(UserCourseBase):
    pass

class UserCourse(UserCourseBase):
    id: UUID
