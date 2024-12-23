from pydantic import BaseModel
from uuid import UUID

class ProgressesBase(BaseModel):
    stage: int
    user_course_id: UUID

class ProgressesCreate(ProgressesBase):
    pass

class Progresses(ProgressesBase):
    id: UUID
