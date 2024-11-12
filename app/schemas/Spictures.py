from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PicturesBase(BaseModel):
    picture: Optional[str] = None 
    exercise_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class PicturesCreate(PicturesBase):
    pass

class Pictures(PicturesBase):
    id: UUID

    class Config:
        from_attributes = True
