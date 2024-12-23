from pydantic import BaseModel
from uuid import UUID

class ViewsBase(BaseModel):
    template: int
    exercise_id: UUID

class ViewsCreate(ViewsBase):
    pass

class Views(ViewsBase):
    id: UUID
