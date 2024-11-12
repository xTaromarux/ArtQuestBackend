from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ViewsBase(BaseModel):
    template: int
    exercise_id: UUID

    class Config:
        from_attributes = True

class ViewsCreate(ViewsBase):
    pass

class ViewsUpdate(ViewsBase):
    pass

class Views(ViewsBase):
    id: UUID

    class Config:
        from_attributes = True
