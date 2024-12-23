from pydantic import BaseModel
from uuid import UUID

class ViewsPicturesBase(BaseModel):
    view_id: UUID
    picture_id: UUID

class ViewsPicturesCreate(ViewsPicturesBase):
    pass

class ViewsPictures(ViewsPicturesBase):
    id: UUID
