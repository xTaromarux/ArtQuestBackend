from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PicturesBase(BaseModel):
    picture: Optional[str] = None 

class PicturesCreate(PicturesBase):
    pass

class Pictures(PicturesBase):
    id: UUID
