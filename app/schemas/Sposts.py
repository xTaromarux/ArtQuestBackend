from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class PostsBase(BaseModel):
    title: str
    description: str
    picture_url: Optional[str] = None  

    class Config:
        from_attributes = True

class PostsCreate(PostsBase):
    pass

class Posts(PostsBase):
    id: UUID
    date_added: datetime
    date_updated: datetime
    user_id: Optional[UUID] = None

    class Config:
        from_attributes = True
