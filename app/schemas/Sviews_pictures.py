from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ViewsPicturesBase(BaseModel):
    view_id: UUID
    picture_id: UUID

    class Config:
        from_attributes = True

class ViewsPicturesCreate(ViewsPicturesBase):
    pass

class ViewsPicturesUpdate(ViewsPicturesBase):
    pass

class ViewsPictures(ViewsPicturesBase):
    id: UUID

    class Config:
        from_attributes = True
