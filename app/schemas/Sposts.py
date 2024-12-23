from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class PostsBase(BaseModel):
    description: Optional[str] = None
    reactions: Optional[int] = None

class PostsCreate(PostsBase):
    pass

class PostsUpdate(BaseModel):
    description: Optional[str] = None

class PostDetailsResponse(BaseModel):
    id: UUID
    description: str
    date_added: datetime
    date_updated: datetime
    reactions: int
    picture_url: Optional[str] = None
    user_name: str
    login: str
    user_picture_url: Optional[str] = None

class Posts(PostsBase):
    id: UUID
    date_added: datetime
    date_updated: datetime
    user_id: Optional[UUID] = None
    picture_id: Optional[UUID] = None
